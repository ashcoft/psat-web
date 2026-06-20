/**
 * Continuation Power Flow (CPF) Module
 * Voltage stability analysis using predictor-corrector method
 */

import { PowerSystem, Bus, Line } from '@/types';
import { solveNewtonRaphson, buildYBus } from './powerflow-methods';

// CPF Configuration
export interface CPFConfig {
  lambdaStart: number;    // Initial loading factor
  lambdaMax: number;      // Maximum loading factor to search
  stepSize: number;       // Initial step size
  stepMin: number;        // Minimum step size
  stepMax: number;        // Maximum step size
  tolerance: number;      // Power mismatch tolerance
  maxIterations: number;   // Max NR iterations per step
  adaptiveStep: boolean;   // Use adaptive step sizing
  targetLambda?: number;   // Target lambda for specific analysis
}

export const defaultCPFConfig: CPFConfig = {
  lambdaStart: 0,
  lambdaMax: 5,
  stepSize: 0.1,
  stepMin: 0.001,
  stepMax: 0.5,
  tolerance: 1e-6,
  maxIterations: 50,
  adaptiveStep: true
};

// CPF Results
export interface CPFResult {
  converged: boolean;
  lambda: number;
  busVoltages: { [busId: string]: number };
  busAngles: { [busId: string]: number };
  lineFlows: { [lineId: string]: number };
  powerMismatch: number;
  iterations: number;
}

export interface CPFHistory {
  results: CPFResult[];
  nosePoint?: CPFResult;
  maximumLoadingPoint?: {
    lambda: number;
    voltages: { [busId: string]: number };
  };
  bifurcationType?: 'saddle-node' | 'limit-induced';
  pvCurve: { lambda: number; v: number }[][];
  vCurve: { lambda: number; v: number }[];
  converged: boolean;
}

export interface VoltageCollapseResult {
  lambdaMax: number;       // Loading margin at collapse point
  criticalBus?: string;    // Bus most susceptible to voltage collapse
  pvCurve: { lambda: number; v: number }[][];
  vCurve: { lambda: number; v: number }[];
  recommendations: string[];
}

/**
 * Create modified power system with increased loading
 */
function scaleLoad(
  system: PowerSystem, 
  lambda: number,
  baseSystem: PowerSystem
): PowerSystem {
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));

  const newLoads = baseSystem.loads.map(load => {
    const busIdx = busIndex.get(load.bus);
    if (busIdx === undefined) return load;
    
    const original = baseSystem.loads.find(l => l.id === load.id);
    const basePl = original?.pl || 0;
    const baseQl = original?.ql || 0;
    
    return {
      ...load,
      pl: basePl * (1 + lambda),
      ql: baseQl * (1 + lambda)
    };
  });

  return {
    ...system,
    loads: newLoads
  };
}

/**
 * Predictor step using tangent vector
 */
function predictorStep(
  system: PowerSystem,
  currentLambda: number,
  currentState: { V: number[]; Theta: number[] },
  stepSize: number,
  baseSystem: PowerSystem
): { newLambda: number; newV: number[]; newTheta: number[]; tangent: number[] } {
  const n = system.buses.length;
  
  // Build augmented Jacobian matrix
  // J_aug = [dP/dTheta  dP/dV  | -Pload]
  //         [dQ/dTheta  dQ/dV  | -Qload]
  //         [dP/dlambda |    0  ]
  //         [dQ/dlambda |    0  ]
  
  const J = buildAugmentedJacobian(system, currentState, currentLambda, baseSystem);
  
  // Right-hand side for tangent vector calculation
  // Solve for tangent vector that gives direction of continuation
  const rhs = new Array(2 * n + 1).fill(0);
  rhs[2 * n] = 1; // Parameter direction
  
  // Solve linear system (simplified)
  const tangent = solveTangentVector(J, rhs, n);
  
  // Predicted next point
  const newLambda = currentLambda + stepSize * tangent[2 * n];
  const newV = currentState.V.map((v, i) => v + stepSize * tangent[n + i]);
  const newTheta = currentState.Theta.map((t, i) => t + stepSize * tangent[i]);
  
  return { newLambda, newV, newTheta, tangent };
}

/**
 * Build augmented Jacobian for CPF
 */
function buildAugmentedJacobian(
  system: PowerSystem,
  state: { V: number[]; Theta: number[] },
  lambda: number,
  baseSystem: PowerSystem
): number[][] {
  const n = system.buses.length;
  const J = Array(2 * n + 1).fill(null).map(() => Array(2 * n + 2).fill(0));
  
  const ybus = buildYBus(system);
  
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const Vi = state.V[i];
      const Vj = state.V[j];
      const thetai = state.Theta[i];
      const thetaj = state.Theta[j];
      const theta_ij = thetai - thetaj;
      
      const gij = ybus.g[i][j];
      const bij = ybus.b[i][j];
      
      // dP/dTheta
      J[i][j] = Vi * Vj * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
      // dP/dV
      J[i][n + j] = Vj * (gij * Math.cos(theta_ij) + bij * Math.sin(theta_ij));
      // dQ/dTheta
      J[n + i][j] = Vi * Vj * (gij * Math.cos(theta_ij) + bij * Math.sin(theta_ij));
      // dQ/dV
      J[n + i][n + j] = Vj * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
    }
  }
  
  // Add parameter column (dP/dLambda, dQ/dLambda)
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  for (const load of baseSystem.loads) {
    const idx = busIndex.get(load.bus);
    if (idx === undefined) continue;
    
    const basePl = load.pl;
    const baseQl = load.ql;
    
    J[idx][2 * n + 1] = -basePl;
    J[n + idx][2 * n + 1] = -baseQl;
  }
  
  return J;
}

/**
 * Solve for tangent vector (simplified)
 */
function solveTangentVector(J: number[][], rhs: number[], n: number): number[] {
  const size = 2 * n + 1;
  const x = new Array(size).fill(0);
  
  // Forward elimination with partial pivoting
  const aug = J.map((row, i) => [...row.slice(0, size), rhs[i]]);
  
  for (let col = 0; col < size; col++) {
    // Find pivot
    let maxRow = col;
    for (let row = col + 1; row < size; row++) {
      if (Math.abs(aug[row][col]) > Math.abs(aug[maxRow][col])) {
        maxRow = row;
      }
    }
    
    // Swap
    [aug[col], aug[maxRow]] = [aug[maxRow], aug[col]];
    
    // Check for singular
    if (Math.abs(aug[col][col]) < 1e-12) {
      aug[col][col] = 1e-12;
    }
    
    // Eliminate
    for (let row = col + 1; row < size; row++) {
      const factor = aug[row][col] / aug[col][col];
      for (let j = col; j <= size; j++) {
        aug[row][j] -= factor * aug[col][j];
      }
    }
  }
  
  // Back substitution
  for (let i = size - 1; i >= 0; i--) {
    x[i] = aug[i][size];
    for (let j = i + 1; j < size; j++) {
      x[i] -= aug[i][j] * x[j];
    }
    x[i] /= aug[i][i];
  }
  
  return x;
}

/**
 * Corrector step using Newton-Raphson with parameter update
 */
function correctorStep(
  system: PowerSystem,
  predictedLambda: number,
  predictedV: number[],
  predictedTheta: number[],
  baseSystem: PowerSystem,
  config: CPFConfig
): CPFResult | null {
  const n = system.buses.length;
  const tolerance = config.tolerance;
  let iter = 0;
  
  let V = [...predictedV];
  let Theta = [...predictedTheta];
  let lambda = predictedLambda;
  
  while (iter < config.maxIterations) {
    // Build power mismatch
    const mismatch = calculateMismatch(system, V, Theta, lambda, baseSystem);
    const maxMismatch = Math.max(...mismatch.map(m => Math.abs(m)));
    
    if (maxMismatch < tolerance) {
      // Converged
      const busVoltages: { [id: string]: number } = {};
      const busAngles: { [id: string]: number } = {};
      
      system.buses.forEach((bus, i) => {
        busVoltages[bus.id] = V[i];
        busAngles[bus.id] = Theta[i] * 180 / Math.PI;
      });
      
      const lineFlows: { [id: string]: number } = {};
      system.lines.forEach(line => {
        lineFlows[line.id] = 0; // Simplified
      });
      
      return {
        converged: true,
        lambda,
        busVoltages,
        busAngles,
        lineFlows,
        powerMismatch: maxMismatch,
        iterations: iter
      };
    }
    
    // Update voltages
    const dV = calculateVoltageUpdate(mismatch, V, Theta, system, baseSystem);
    for (let i = 0; i < n; i++) {
      V[i] = Math.max(0.1, Math.min(2.0, V[i] + dV[i]));
    }
    
    iter++;
  }
  
  return null; // Did not converge
}

/**
 * Calculate power mismatch
 */
function calculateMismatch(
  system: PowerSystem,
  V: number[],
  Theta: number[],
  lambda: number,
  baseSystem: PowerSystem
): number[] {
  const n = system.buses.length;
  const mismatch = new Array(2 * n).fill(0);
  
  const ybus = buildYBus(system);
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  for (let i = 0; i < n; i++) {
    let Pi = 0;
    let Qi = 0;
    
    for (let j = 0; j < n; j++) {
      const Vi = V[i];
      const Vj = V[j];
      const theta_ij = Theta[i] - Theta[j];
      
      const gij = ybus.g[i][j];
      const bij = ybus.b[i][j];
      
      Pi += Vi * Vj * (gij * Math.cos(theta_ij) + bij * Math.sin(theta_ij));
      Qi += Vi * Vj * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
    }
    
    // Add load component
    const load = system.loads.find(l => busIndex.get(l.bus) === i);
    const basePl = baseSystem.loads.find(l => l.bus === system.buses[i].id)?.pl || 0;
    const baseQl = baseSystem.loads.find(l => l.bus === system.buses[i].id)?.ql || 0;
    const totalPl = basePl * (1 + lambda);
    const totalQl = baseQl * (1 + lambda);
    
    mismatch[i] = Pi - totalPl;
    mismatch[n + i] = Qi - totalQl;
  }
  
  return mismatch;
}

/**
 * Calculate voltage update (simplified Newton step)
 */
function calculateVoltageUpdate(
  mismatch: number[],
  V: number[],
  Theta: number[],
  system: PowerSystem,
  baseSystem: PowerSystem
): number[] {
  const n = system.buses.length;
  const dV = new Array(n).fill(0);
  
  // Simplified: use Q mismatch to update voltage
  for (let i = 0; i < n; i++) {
    dV[i] = -mismatch[n + i] / (V[i] + 0.1);
  }
  
  return dV;
}

/**
 * Run Continuation Power Flow
 */
export function runCPF(
  system: PowerSystem,
  config: Partial<CPFConfig> = {}
): CPFHistory {
  const cfg = { ...defaultCPFConfig, ...config };
  const baseSystem = JSON.parse(JSON.stringify(system));
  
  const results: CPFResult[] = [];
  let lambda = cfg.lambdaStart;
  let stepSize = cfg.stepSize;
  
  // Initialize state
  const initialResult = solveNewtonRaphson(system);
  if (!initialResult.converged) {
    return { results: [], converged: false, pvCurve: [], vCurve: [] };
  }
  
  let V = system.buses.map(b => b.voltage || 1.0);
  let Theta = system.buses.map(b => (b.angle || 0) * Math.PI / 180);
  
  // Store initial point
  results.push({
    converged: true,
    lambda: 0,
    busVoltages: system.buses.reduce((acc, b, i) => ({ ...acc, [b.id]: V[i] }), {}),
    busAngles: system.buses.reduce((acc, b, i) => ({ ...acc, [b.id]: Theta[i] * 180 / Math.PI }), {}),
    lineFlows: {},
    powerMismatch: 0,
    iterations: 0
  });
  
  // Main continuation loop
  while (lambda < cfg.lambdaMax) {
    // Create scaled system
    const scaledSystem = scaleLoad(system, lambda, baseSystem);
    
    // Predictor step
    const prediction = predictorStep(scaledSystem, lambda, { V, Theta }, stepSize, baseSystem);
    
    // Corrector step
    const corrected = correctorStep(scaledSystem, prediction.newLambda, prediction.newV, prediction.newTheta, baseSystem, cfg);
    
    if (corrected && corrected.converged) {
      results.push(corrected);
      
      // Update state
      lambda = corrected.lambda;
      V = system.buses.map(b => corrected.busVoltages[b.id] || 1.0);
      Theta = system.buses.map(b => (corrected.busAngles[b.id] || 0) * Math.PI / 180);
      
      // Adaptive step sizing
      if (cfg.adaptiveStep) {
        const voltageDrop = 1.0 - V.reduce((min, v) => Math.min(min, v), 1.0);
        if (voltageDrop > 0.05) {
          stepSize = Math.max(cfg.stepMin, stepSize * 0.8);
        } else if (voltageDrop < 0.01) {
          stepSize = Math.min(cfg.stepMax, stepSize * 1.2);
        }
      }
      
      // Check for voltage collapse (very low voltage)
      const minV = V.reduce((min, v) => Math.min(min, v), 1.0);
      if (minV < 0.5) {
        break; // Near collapse
      }
    } else {
      // Reduce step size and retry
      stepSize = Math.max(cfg.stepMin, stepSize * 0.5);
      if (stepSize <= cfg.stepMin) {
        break; // Can't make progress
      }
    }
  }
  
  // Find nose point (maximum loading)
  let nosePoint: CPFResult | undefined;
  let maxLambda = 0;
  
  results.forEach(r => {
    if (r.lambda > maxLambda) {
      maxLambda = r.lambda;
      nosePoint = r;
    }
  });
  
  // Build PV curve
  const pvCurve = system.buses.map(bus => {
    const busIdx = system.buses.findIndex(b => b.id === bus.id);
    return results.map(r => ({
      lambda: r.lambda,
      v: V[busIdx] || 1.0
    }));
  });
  
  const vCurve = results.map(r => {
    // Use reference bus or lowest voltage bus
    const refBus = system.buses[0];
    return {
      lambda: r.lambda,
      v: r.busVoltages[refBus.id] || 1.0
    };
  });
  
  return {
    results,
    nosePoint,
    maximumLoadingPoint: nosePoint ? {
      lambda: nosePoint.lambda,
      voltages: nosePoint.busVoltages
    } : undefined,
    pvCurve,
    vCurve,
    converged: results.length > 0
  };
}

/**
 * Analyze voltage collapse
 */
export function analyzeVoltageCollapse(system: PowerSystem): VoltageCollapseResult {
  const cpfResult = runCPF(system);
  
  // Find critical bus (lowest voltage at nose point)
  let criticalBus: string | undefined;
  let minV = 1.0;
  
  if (cpfResult.nosePoint) {
    Object.entries(cpfResult.nosePoint.busVoltages).forEach(([busId, v]) => {
      if (v < minV) {
        minV = v;
        criticalBus = busId;
      }
    });
  }
  
  const recommendations: string[] = [];
  
  if (cpfResult.nosePoint && cpfResult.nosePoint.lambda < 2) {
    recommendations.push('Low loading margin - system is vulnerable to voltage collapse');
    recommendations.push('Consider adding reactive power support');
    recommendations.push('Evaluate shunt compensation');
  }
  
  if (cpfResult.nosePoint && cpfResult.nosePoint.lambda > 3) {
    recommendations.push('Adequate loading margin');
  }
  
  if (criticalBus) {
    recommendations.push(`Critical bus identified: ${criticalBus}`);
    recommendations.push('Prioritize voltage support at this bus');
  }
  
  return {
    lambdaMax: cpfResult.nosePoint?.lambda || 0,
    criticalBus,
    pvCurve: cpfResult.pvCurve,
    vCurve: cpfResult.vCurve,
    recommendations
  };
}

/**
 * Calculate L-index for voltage stability
 */
export function calculateLIndex(system: PowerSystem): { L: number[]; Lmax: number; stable: boolean } {
  const pfResult = solveNewtonRaphson(system);
  
  if (!pfResult.converged) {
    return { L: [], Lmax: 0, stable: false };
  }
  
  const n = system.buses.length;
  const L: number[] = [];
  
  // Simplified L-index calculation
  for (let i = 0; i < n; i++) {
    const Vi = pfResult.busResults[i]?.v || 1.0;
    const Vi_pu = Vi;
    
    // L-index: proximity to voltage instability
    // L = |1 - V_i / V_slack|
    const bus = system.buses[i];
    if (bus.type !== 'slack') {
      const L_i = Math.abs(1 - Vi_pu);
      L.push(L_i);
    }
  }
  
  const Lmax = L.length > 0 ? Math.max(...L) : 0;
  const stable = Lmax < 0.2; // Threshold
  
  return { L, Lmax, stable };
}

/**
 * P-V curve data for visualization
 */
export function generatePVData(system: PowerSystem, busId: string): { p: number[]; v: number[] } {
  const cpfResult = runCPF(system);
  
  const p: number[] = [];
  const v: number[] = [];
  
  cpfResult.results.forEach(r => {
    p.push(r.lambda * 100); // Convert to percentage loading
    v.push(r.busVoltages[busId] || 1.0);
  });
  
  return { p, v };
}
