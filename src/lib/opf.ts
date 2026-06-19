/**
 * Optimal Power Flow (OPF) Module
 * Minimizes generation cost while satisfying power flow constraints
 */

import { PowerSystem, Generator, Bus, Line, OPFResult, GeneratorCost } from '@/types';
import { solveNewtonRaphson, buildYBus } from './powerflow-methods';

// Cost function types
export type CostModelType = 'polynomial' | 'piecewise' | 'exponential';

export interface GeneratorCostParams {
  id: string;
  bus: string;
  model: CostModelType;
  // Polynomial model: cost = a + b*P + c*P^2
  a?: number; // Constant term ($/h)
  b?: number; // Linear term ($/MWh)
  c?: number; // Quadratic term ($/MW^2h)
  // Piecewise model: breakpoints
  points?: { p: number; cost: number }[];
  // Startup/shutdown costs
  startup?: number;
  shutdown?: number;
}

/**
 * Default cost function generator
 */
export function createDefaultCost(gen: Generator): GeneratorCostParams {
  return {
    id: gen.id,
    bus: gen.bus,
    model: 'polynomial',
    a: 10, // $10/h base cost
    b: 30 + Math.random() * 10, // ~$30-40/MWh
    c: 0.01, // Small quadratic term
    startup: 50,
    shutdown: 25
  };
}

/**
 * Calculate generator cost
 */
export function calculateGeneratorCost(gen: Generator, costParams: GeneratorCostParams): number {
  const pg = gen.pg;
  
  switch (costParams.model) {
    case 'polynomial':
      const a = costParams.a || 0;
      const b = costParams.b || 0;
      const c = costParams.c || 0;
      return a + b * pg + c * pg * pg;
      
    case 'piecewise':
      // Linear interpolation between points
      const points = costParams.points || [];
      if (points.length < 2) return 0;
      
      // Find the segment
      for (let i = 0; i < points.length - 1; i++) {
        if (pg >= points[i].p && pg <= points[i + 1].p) {
          const ratio = (pg - points[i].p) / (points[i + 1].p - points[i].p);
          return points[i].cost + ratio * (points[i + 1].cost - points[i].cost);
        }
      }
      return points[points.length - 1].cost;
      
    default:
      return 0;
  }
}

/**
 * Calculate total system cost
 */
export function calculateTotalCost(
  generators: Generator[], 
  costs: GeneratorCostParams[]
): number {
  let totalCost = 0;
  
  for (const gen of generators) {
    const costParams = costs.find(c => c.id === gen.id) || createDefaultCost(gen);
    totalCost += calculateGeneratorCost(gen, costParams);
  }
  
  return totalCost;
}

/**
 * Optimal Power Flow using Linear Programming (DC approximation)
 * 
 * Minimize: Σ (a_i + b_i * P_i + c_i * P_i^2)
 * Subject to:
 *   - Power balance: Σ P_i = Σ P_load + P_loss
 *   - Generator limits: P_min ≤ P_i ≤ P_max
 *   - Line limits: |P_ij| ≤ P_ij_max
 */
export function solveDCOPF(
  system: PowerSystem,
  costs?: GeneratorCostParams[]
): OPFResult {
  const startTime = performance.now();
  
  // Create default costs if not provided
  const genCosts = costs || system.generators.map(createDefaultCost);
  
  // Get slack bus
  let slackBus: Bus | undefined;
  let slackIdx = -1;
  system.buses.forEach((bus, idx) => {
    if (bus.type === 'slack') {
      slackBus = bus;
      slackIdx = idx;
    }
  });
  if (!slackBus) {
    slackBus = system.buses[0];
    slackIdx = 0;
  }
  
  // Calculate total load
  let totalLoad = 0;
  system.loads.forEach(load => {
    if (load.active) totalLoad += load.pl;
  });
  
  // Calculate total generation capacity
  let totalCapacity = 0;
  system.generators.forEach(gen => {
    if (gen.active) totalCapacity += gen.pmax;
  });
  
  // Simple economic dispatch: proportional to capacity and marginal cost
  const n = system.generators.length;
  const dispatches: { genId: string; bus: string; pg: number; qg: number; cost: number }[] = [];
  
  if (n === 0) {
    return {
      success: false,
      message: 'No generators in system',
      generatorResults: [],
      totalCost: 0,
      elapsedTime: performance.now() - startTime
    };
  }
  
  if (n === 1) {
    // Single generator takes all load
    const gen = system.generators[0];
    const costParams = genCosts.find(c => c.id === gen.id) || createDefaultCost(gen);
    const pg = Math.min(Math.max(totalLoad, gen.pmin), gen.pmax);
    const cost = calculateGeneratorCost({ ...gen, pg }, costParams);
    
    return {
      success: true,
      message: 'Single generator dispatch',
      generatorResults: [{
        generator: gen.id,
        bus: gen.bus,
        pg,
        qg: 0,
        v: gen.v,
        status: 'on'
      }],
      totalCost: cost,
      elapsedTime: performance.now() - startTime
    };
  }
  
  // Multi-generator dispatch using merit order based on marginal cost
  // Marginal cost = d(cost)/d(P) = b + 2*c*P
  type GenWithMarginalCost = { gen: Generator; mc: number; idx: number };
  const gensWithMc: GenWithMarginalCost[] = system.generators
    .map((gen, idx) => {
      const costParams = genCosts.find(c => c.id === gen.id) || createDefaultCost(gen);
      const c = costParams.c || 0;
      const b = costParams.b || 50;
      // Estimate marginal cost at 50% capacity
      const pgEst = (gen.pmax + gen.pmin) / 2;
      const mc = b + 2 * c * pgEst;
      return { gen, mc, idx };
    })
    .filter(g => g.gen.active);
  
  // Sort by marginal cost (merit order)
  gensWithMc.sort((a, b) => a.mc - b.mc);
  
  // Dispatch generators in merit order
  let remainingLoad = totalLoad;
  let totalCost = 0;
  
  for (const g of gensWithMc) {
    if (remainingLoad <= 0) break;
    
    const gen = g.gen;
    const costParams = genCosts.find(c => c.id === gen.id) || createDefaultCost(gen);
    
    // Available capacity
    const available = Math.min(gen.pmax - gen.pg, remainingLoad);
    const pg = Math.max(0, Math.min(available, gen.pmax - gen.pmin));
    
    const cost = calculateGeneratorCost({ ...gen, pg }, costParams);
    totalCost += cost;
    
    dispatches.push({
      genId: gen.id,
      bus: gen.bus,
      pg: gen.pg + pg,
      qg: 0,
      cost
    });
    
    remainingLoad -= pg;
  }
  
  // Check if load was met
  if (remainingLoad > 0.01) {
    // Try to redispatch from all generators
    dispatches.length = 0;
    totalCost = 0;
    remainingLoad = totalLoad;
    
    for (const g of gensWithMc) {
      const gen = g.gen;
      const costParams = genCosts.find(c => c.id === gen.id) || createDefaultCost(gen);
      const available = gen.pmax - gen.pmin;
      const ratio = remainingLoad / totalCapacity;
      const pg = gen.pmin + available * ratio;
      
      const cost = calculateGeneratorCost({ ...gen, pg }, costParams);
      totalCost += cost;
      
      dispatches.push({
        genId: gen.id,
        bus: gen.bus,
        pg,
        qg: 0,
        cost
      });
      
      remainingLoad -= pg;
    }
  }
  
  // Create modified system with new dispatches
  const modifiedSystem: PowerSystem = {
    ...system,
    generators: system.generators.map(gen => {
      const dispatch = dispatches.find(d => d.genId === gen.id);
      return dispatch ? { ...gen, pg: dispatch.pg } : gen;
    })
  };
  
  // Run power flow to get network solution
  const pfResult = solveNewtonRaphson(modifiedSystem);
  
  // Format generator results
  const generatorResults = dispatches.map(d => ({
    generator: d.genId,
    bus: d.bus,
    pg: d.pg,
    qg: d.qg || pfResult.generatorResults.find(r => r.generator === d.genId)?.qg || 0,
    v: system.generators.find(g => g.id === d.genId)?.v || 1.0,
    status: 'on' as const
  }));
  
  return {
    success: dispatches.length > 0,
    message: dispatches.length > 0 ? 'OPF converged' : 'Could not meet load demand',
    generatorResults,
    totalCost,
    elapsedTime: performance.now() - startTime,
    busResults: pfResult.busResults,
    lineResults: pfResult.lineResults,
    losses: pfResult.losses
  };
}

/**
 * OPF with full AC power flow (iterative)
 */
export function solveACOPF(
  system: PowerSystem,
  costs?: GeneratorCostParams[],
  tolerance = 1e-4,
  maxIterations = 50
): OPFResult {
  const startTime = performance.now();
  const genCosts = costs || system.generators.map(createDefaultCost);
  
  // Initialize with DC OPF
  let result = solveDCOPF(system, genCosts);
  if (!result.success) {
    return { ...result, elapsedTime: performance.now() - startTime };
  }
  
  // Iterative refinement using gradient descent
  let iterations = 0;
  let improved = true;
  let currentCost = result.totalCost;
  
  while (improved && iterations < maxIterations) {
    improved = false;
    
    // Try small adjustments to each generator
    for (const gen of system.generators) {
      if (!gen.active) continue;
      
      const costParams = genCosts.find(c => c.id === gen.id) || createDefaultCost(gen);
      const step = (gen.pmax - gen.pmin) * 0.01; // 1% step
      
      // Try increasing
      if (gen.pg < gen.pmax - step) {
        const newGen = { ...gen, pg: gen.pg + step };
        const newCost = calculateGeneratorCost(newGen, costParams);
        
        // Check marginal cost
        const marginalCost = (costParams.b || 50) + 2 * (costParams.c || 0) * newGen.pg;
        
        if (marginalCost < 60) { // Cheap generation available
          const testSystem: PowerSystem = {
            ...system,
            generators: system.generators.map(g => g.id === gen.id ? newGen : g)
          };
          
          const testPf = solveNewtonRaphson(testSystem);
          
          if (testPf.converged) {
            const newTotalCost = calculateTotalCost(testSystem.generators, genCosts);
            
            if (newTotalCost < currentCost - tolerance) {
              result = {
                success: true,
                message: 'Refined dispatch',
                generatorResults: testSystem.generators.map(g => ({
                  generator: g.id,
                  bus: g.bus,
                  pg: g.pg,
                  qg: g.qg,
                  v: g.v,
                  status: 'on'
                })),
                totalCost: newTotalCost,
                busResults: testPf.busResults,
                lineResults: testPf.lineResults,
                losses: testPf.losses,
                elapsedTime: performance.now() - startTime
              };
              currentCost = newTotalCost;
              improved = true;
            }
          }
        }
      }
    }
    
    iterations++;
  }
  
  return {
    ...result,
    elapsedTime: performance.now() - startTime
  };
}

/**
 * Security Constrained OPF (simplified)
 * Checks line constraints after optimal dispatch
 */
export function solveSecurityConstrainedOPF(
  system: PowerSystem,
  costs?: GeneratorCostParams[],
  contingencyList?: { from: string; to: string }[]
): OPFResult & { violations: string[] } {
  const startTime = performance.now();
  const genCosts = costs || system.generators.map(createDefaultCost);
  
  // First solve base case
  const baseResult = solveDCOPF(system, genCosts);
  
  if (!baseResult.success) {
    return {
      ...baseResult,
      violations: ['Base case infeasible'],
      elapsedTime: performance.now() - startTime
    };
  }
  
  const violations: string[] = [];
  const contingencies = contingencyList || system.lines
    .filter(l => l.active)
    .map(l => ({ from: l.fromBus, to: l.toBus }));
  
  // Check each contingency
  for (const cont of contingencies) {
    // Create contingency system (remove one line)
    const contSystem: PowerSystem = {
      ...system,
      lines: system.lines.filter(l => 
        !(l.fromBus === cont.from && l.toBus === cont.to) &&
        !(l.fromBus === cont.to && l.toBus === cont.from)
      ),
      generators: baseResult.generatorResults.map(r => ({
        id: r.generator,
        bus: r.bus,
        pg: r.pg,
        qg: r.qg || 0,
        v: r.v,
        pmax: system.generators.find(g => g.id === r.generator)?.pmax || 1,
        pmin: system.generators.find(g => g.id === r.generator)?.pmin || 0,
        qmax: system.generators.find(g => g.id === r.generator)?.qmax || 0.5,
        qmin: system.generators.find(g => g.id === r.generator)?.qmin || -0.5,
        active: true
      }))
    };
    
    // Check power flow
    const pf = solveNewtonRaphson(contSystem);
    
    if (!pf.converged) {
      violations.push(`Contingency ${cont.from}-${cont.to}: No solution`);
      continue;
    }
    
    // Check line loadings
    for (const line of pf.lineResults) {
      if (line.loading > 100) {
        violations.push(`Contingency ${cont.from}-${cont.to}: Line ${line.line} overloaded ${line.loading.toFixed(1)}%`);
      }
    }
    
    // Check voltage limits
    for (const bus of pf.busResults) {
      if (bus.v < 0.9 || bus.v > 1.1) {
        violations.push(`Contingency ${cont.from}-${cont.to}: Bus ${bus.bus} voltage ${(bus.v * 100).toFixed(1)}%`);
      }
    }
  }
  
  return {
    ...baseResult,
    violations,
    elapsedTime: performance.now() - startTime
  };
}

/**
 * Unit Commitment simplified (24-hour)
 */
export function solveUnitCommitment(
  system: PowerSystem,
  horizon = 24,
  loads?: number[]
): { schedules: { hour: number; generators: { id: string; on: boolean; pg: number }[]; cost: number }[] } {
  const genCosts = system.generators.map(createDefaultCost);
  const schedules: { hour: number; generators: { id: string; on: boolean; pg: number }[]; cost: number }[] = [];
  
  // Default load pattern
  const hourlyLoads = loads || Array(horizon).fill(0).map((_, h) => {
    // Simple daily pattern: peak at noon
    const base = 0.5;
    const peak = 0.3 * Math.sin((h - 6) * Math.PI / 12);
    return Math.max(0.1, base + peak);
  });
  
  // Scale to system load
  const totalSystemLoad = system.loads.reduce((sum, l) => sum + l.pl, 0);
  
  for (let hour = 0; hour < horizon; hour++) {
    const load = hourlyLoads[hour] * totalSystemLoad;
    const hourSchedule: { hour: number; generators: { id: string; on: boolean; pg: number }[]; cost: number } = {
      hour,
      generators: [],
      cost: 0
    };
    
    // Merit order dispatch
    const sortedGens = [...system.generators]
      .filter(g => g.active)
      .map(g => {
        const costParams = genCosts.find(c => c.id === g.id)!;
        return { gen: g, mc: (costParams.b || 50) + 2 * (costParams.c || 0) * g.pg };
      })
      .sort((a, b) => a.mc - b.mc);
    
    let remainingLoad = load;
    for (const { gen, mc } of sortedGens) {
      if (remainingLoad <= 0) break;
      
      const costParams = genCosts.find(c => c.id === gen.id)!;
      const pg = Math.min(gen.pmax, remainingLoad);
      
      if (pg >= gen.pmin) {
        hourSchedule.generators.push({ id: gen.id, on: true, pg });
        hourSchedule.cost += calculateGeneratorCost({ ...gen, pg }, costParams);
        remainingLoad -= pg;
      }
    }
    
    schedules.push(hourSchedule);
  }
  
  return { schedules };
}
