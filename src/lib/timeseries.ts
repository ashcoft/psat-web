/**
 * Time Domain Simulation Module
 * Dynamic simulation of power systems using numerical integration
 */

import { PowerSystem, Generator, Load, Bus } from '@/types';

// Simulation types
export type IntegrationMethod = 'euler' | 'rk4' | 'rk45' | 'trapezoidal';

export interface SimulationConfig {
  tStart: number;
  tEnd: number;
  dt: number;
  method: IntegrationMethod;
  outputInterval: number;
  faultTime?: number;
  faultDuration?: number;
  loadChangeTime?: number;
  loadChangeFactor?: number;
}

export interface TimeSeriesResult {
  time: number[];
  busVoltages: { [busId: string]: number[] };
  busAngles: { [busId: string]: number[] };
  generatorAngles: { [genId: string]: number[] };
  generatorSpeeds: { [genId: string]: number[] };
  lineFlows: { [lineId: string]: { p: number[]; q: number[] } };
  busFrequencies: { [busId: string]: number[] };
}

export interface DynamicBusState {
  v: number;        // Voltage magnitude (pu)
  angle: number;    // Voltage angle (rad)
  omega: number;    // Rotor speed (pu, 1.0 = nominal)
  delta: number;    // Rotor angle (rad)
  eq: number;       // Internal EMF (pu)
  ed: number;       // Direct axis EMF component
}

export interface DynamicSystemState {
  buses: DynamicBusState[];
  time: number;
}

// Default configuration
export const defaultSimulationConfig: SimulationConfig = {
  tStart: 0,
  tEnd: 5,
  dt: 0.01,
  method: 'rk4',
  outputInterval: 0.05
};

/**
 * Synchronous generator model (simplified swing equation)
 */
export interface GeneratorModel {
  id: string;
  bus: string;
  H: number;      // Inertia constant (s)
  D: number;      // Damping coefficient
  Pm: number;     // Mechanical power input (pu)
  Pe: number;     // Electrical power output (pu)
  omega: number;  // Rotor speed (pu)
  delta: number;  // Rotor angle (rad)
  Pmax?: number;  // Maximum power (for stability limit)
}

/**
 * Create generator models from system data
 */
export function createGeneratorModels(system: PowerSystem): GeneratorModel[] {
  return system.generators
    .filter(g => g.active)
    .map(g => ({
      id: g.id,
      bus: g.bus,
      H: (g as any).inertia ?? 3.5, // Deterministic default H
      D: (g as any).damping ?? 1.5,  // Deterministic default D
      Pm: g.pg / (system.baseMVA || 100),
      Pe: 0,
      omega: 1.0,
      delta: 0,
      Pmax: g.pmax * 1.2
    }));
}

/**
 * Swing equation derivatives
 * d(delta)/dt = omega - omega_s
 * d(omega)/dt = (Pm - Pe - D*(omega - omega_s)) / (2*H)
 */
function swingEquationDerivative(state: GeneratorModel): { dDelta: number; dOmega: number } {
  const omega_s = 1.0; // Synchronous speed (pu)
  const dDelta = state.omega - omega_s;
  const dOmega = (state.Pm - state.Pe - state.D * (state.omega - omega_s)) / (2 * state.H);
  
  return { dDelta, dOmega };
}

/**
 * Euler integration step
 */
function eulerStep(gen: GeneratorModel, dt: number): void {
  const { dDelta, dOmega } = swingEquationDerivative(gen);
  gen.delta += dt * dDelta;
  gen.omega += dt * dOmega;
}

/**
 * Runge-Kutta 4th order integration step
 */
function rk4Step(gen: GeneratorModel, dt: number): void {
  const omega_s = 1.0;
  
  // k1
  const k1_dDelta = gen.omega - omega_s;
  const k1_dOmega = (gen.Pm - gen.Pe - gen.D * (gen.omega - omega_s)) / (2 * gen.H);
  
  // k2
  const omega2 = gen.omega + 0.5 * dt * k1_dOmega;
  const delta2 = gen.delta + 0.5 * dt * k1_dDelta;
  const k2_dDelta = omega2 - omega_s;
  const k2_dOmega = (gen.Pm - gen.Pe - gen.D * (omega2 - omega_s)) / (2 * gen.H);
  
  // k3
  const omega3 = gen.omega + 0.5 * dt * k2_dOmega;
  const delta3 = gen.delta + 0.5 * dt * k2_dDelta;
  const k3_dDelta = omega3 - omega_s;
  const k3_dOmega = (gen.Pm - gen.Pe - gen.D * (omega3 - omega_s)) / (2 * gen.H);
  
  // k4
  const omega4 = gen.omega + dt * k3_dOmega;
  const delta4 = gen.delta + dt * k3_dDelta;
  const k4_dDelta = omega4 - omega_s;
  const k4_dOmega = (gen.Pm - gen.Pe - gen.D * (omega4 - omega_s)) / (2 * gen.H);
  
  // Update
  gen.delta += (dt / 6) * (k1_dDelta + 2 * k2_dDelta + 2 * k3_dDelta + k4_dDelta);
  gen.omega += (dt / 6) * (k1_dOmega + 2 * k2_dOmega + 2 * k3_dOmega + k4_dOmega);
}

/**
 * Calculate electrical power from voltage and impedance
 */
function calculateElectricalPower(
  gen: GeneratorModel,
  buses: Bus[],
  V: Map<string, number>,
  Theta: Map<string, number>
): number {
  const bus = buses.find(b => b.id === gen.bus);
  if (!bus) return 0;
  
  const Vg = V.get(gen.bus) || 1.0;
  const thetag = Theta.get(gen.bus) || 0;
  const Eg = 1.0; // Internal voltage (simplified)
  const Xd = 0.3; // Transient reactance
  
  // Pe = Eg * Vg * sin(delta - theta) / Xd
  const Pe = (Eg * Vg * Math.sin(gen.delta - thetag)) / Xd;
  return Math.max(0, Math.min(Pe, gen.Pmax || Infinity));
}

/**
 * Run time domain simulation
 */
export function runTimeDomainSimulation(
  system: PowerSystem,
  config: Partial<SimulationConfig> = {}
): TimeSeriesResult {
  const cfg = { ...defaultSimulationConfig, ...config };
  
  // Initialize generator models
  const generators = createGeneratorModels(system);
  
  // Initialize voltage/angle tracking
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  // Initialize state arrays
  const V = new Map<string, number>();
  const Theta = new Map<string, number>();
  system.buses.forEach(b => {
    V.set(b.id, b.voltage || 1.0);
    Theta.set(b.id, (b.angle || 0) * Math.PI / 180);
  });
  
  // Output arrays
  const time: number[] = [];
  const busVoltages: { [key: string]: number[] } = {};
  const busAngles: { [key: string]: number[] } = {};
  const generatorAngles: { [key: string]: number[] } = {};
  const generatorSpeeds: { [key: string]: number[] } = {};
  const lineFlows: { [key: string]: { p: number[]; q: number[] } } = {};
  const busFrequencies: { [key: string]: number[] } = {};
  
  // Initialize output maps
  system.buses.forEach(b => {
    busVoltages[b.id] = [];
    busAngles[b.id] = [];
    busFrequencies[b.id] = [];
  });
  generators.forEach(g => {
    generatorAngles[g.id] = [];
    generatorSpeeds[g.id] = [];
  });
  system.lines.forEach(l => {
    lineFlows[l.id] = { p: [], q: [] };
  });
  
  // Initial power flow solution
  // Simplified: assume all generators share load proportionally
  const totalLoad = system.loads.reduce((sum, l) => sum + l.pl, 0);
  generators.forEach(g => {
    const ratio = g.Pm / (generators.reduce((s, g) => s + g.Pm, 0) || 1);
    g.Pm = ratio * totalLoad / (system.baseMVA || 100);
  });
  
  // Simulation loop
  let t = cfg.tStart;
  let nextOutputTime = cfg.tStart;
  let lastOutputIdx = 0;
  let loadChangeApplied = false;
  
  while (t <= cfg.tEnd) {
    // Apply events
    if (cfg.faultTime && t >= cfg.faultTime && t < cfg.faultTime + (cfg.faultDuration || 0.1)) {
      // Apply fault - reduce voltage at faulted bus
      const faultBus = '1'; // Assume fault at slack bus
      V.set(faultBus, 0.1);
    }
    
    if (cfg.loadChangeTime && t >= cfg.loadChangeTime && !loadChangeApplied) {
      // Apply load change (only once)
      const factor = cfg.loadChangeFactor || 1.2;
      generators.forEach(g => {
        g.Pm *= factor;
      });
      loadChangeApplied = true;
    }
    
    // Calculate electrical power for each generator
    generators.forEach(g => {
      g.Pe = calculateElectricalPower(g, system.buses, V, Theta);
    });
    
    // Integration step
    switch (cfg.method) {
      case 'euler':
        generators.forEach(g => eulerStep(g, cfg.dt));
        break;
      case 'rk4':
      default:
        generators.forEach(g => rk4Step(g, cfg.dt));
        break;
    }
    
    // Clamp frequencies
    generators.forEach(g => {
      g.omega = Math.max(0.9, Math.min(1.1, g.omega));
    });
    
    // Update bus states (simplified voltage decay)
    system.buses.forEach(b => {
      const currentV = V.get(b.id) || 1.0;
      const targetV = b.voltage || 1.0;
      if (!cfg.faultTime || t < cfg.faultTime || t >= cfg.faultTime + (cfg.faultDuration || 0.1)) {
        V.set(b.id, currentV + 0.1 * (targetV - currentV) * cfg.dt);
      }
      
      const currentTheta = Theta.get(b.id) || 0;
      // Angle drifts based on frequency deviation
      const genOnBus = generators.find(g => g.bus === b.id);
      const omegaDev = genOnBus ? genOnBus.omega - 1.0 : 0;
      Theta.set(b.id, currentTheta + omegaDev * cfg.dt * 2 * Math.PI * 60);
    });
    
    t += cfg.dt;
    
    // Store output at specified intervals
    if (t >= nextOutputTime) {
      time.push(t);
      
      system.buses.forEach(b => {
        busVoltages[b.id].push(V.get(b.id) || 1.0);
        busAngles[b.id].push((Theta.get(b.id) || 0) * 180 / Math.PI);
        const genOnBus = generators.find(g => g.bus === b.id);
        const omega = genOnBus ? genOnBus.omega : 1.0;
        busFrequencies[b.id].push(omega * 60);
      });
      
      generators.forEach(g => {
        generatorAngles[g.id].push(g.delta * 180 / Math.PI);
        generatorSpeeds[g.id].push(g.omega * 60);
      });
      
      // Calculate line flows (simplified)
      system.lines.forEach(l => {
        const Vi = V.get(l.fromBus) || 1.0;
        const Vj = V.get(l.toBus) || 1.0;
        const thetai = Theta.get(l.fromBus) || 0;
        const thetaj = Theta.get(l.toBus) || 0;
        const dTheta = thetai - thetaj;
        const z = Math.sqrt(l.resistance ** 2 + l.reactance ** 2);
        const I = (Vi - Vj) / (l.resistance + l.reactance);
        const P = Vi * I;
        lineFlows[l.id].p.push(P * (system.baseMVA || 100));
        lineFlows[l.id].q.push(0);
      });
      
      nextOutputTime += cfg.outputInterval;
    }
  }
  
  return {
    time,
    busVoltages,
    busAngles,
    generatorAngles,
    generatorSpeeds,
    lineFlows,
    busFrequencies
  };
}

/**
 * Run multiple simulations with different contingencies
 */
export function runContingencyStudy(
  system: PowerSystem,
  contingencies: {
    name: string;
    faultBus?: string;
    faultTime?: number;
    faultDuration?: number;
    loadChange?: { time: number; factor: number };
  }[]
): { name: string; result: TimeSeriesResult }[] {
  return contingencies.map(cont => ({
    name: cont.name,
    result: runTimeDomainSimulation(system, {
      tStart: 0,
      tEnd: 5,
      dt: 0.01,
      method: 'rk4',
      outputInterval: 0.05,
      faultTime: cont.faultTime,
      faultDuration: cont.faultDuration,
      loadChangeTime: cont.loadChange?.time,
      loadChangeFactor: cont.loadChange?.factor
    })
  }));
}

/**
 * Check stability from time series
 */
export function checkStability(result: TimeSeriesResult): {
  stable: boolean;
  minOmega: number;
  maxOmega: number;
  criticalTime?: number;
} {
  const allSpeeds = Object.values(result.generatorSpeeds).flat();
  
  if (allSpeeds.length === 0) {
    return { stable: true, minOmega: 60, maxOmega: 60 };
  }
  
  const minOmega = Math.min(...allSpeeds);
  const maxOmega = Math.max(...allSpeeds);
  
  // Check for instability (frequency outside 59-61 Hz for too long)
  let criticalTime: number | undefined;
  for (let i = 0; i < result.time.length; i++) {
    const speeds = Object.values(result.generatorSpeeds).map(s => s[i]);
    if (speeds.some(s => s < 59.5 || s > 60.5)) {
      criticalTime = result.time[i];
      break;
    }
  }
  
  const stable = minOmega > 59.5 && maxOmega < 60.5 && !criticalTime;
  
  return { stable, minOmega, maxOmega, criticalTime };
}

/**
 * Calculate critical clearing time (simplified)
 */
export function calculateCriticalClearingTime(
  system: PowerSystem,
  faultBus: string = '1'
): {cct: number; faultTime: number; cctRange: [number, number]} {
  const faultDuration = 0.05; // 50ms initial guess
  const maxDuration = 1.0;
  const tolerance = 0.01;
  
  let low = faultDuration;
  let high = maxDuration;
  let cct = faultDuration;
  
  // Binary search for CCT
  while (high - low > tolerance) {
    const mid = (low + high) / 2;
    
    const result = runTimeDomainSimulation(system, {
      tStart: 0,
      tEnd: 3,
      dt: 0.01,
      method: 'rk4',
      outputInterval: 0.05,
      faultTime: 0.1,
      faultDuration: mid
    });
    
    const { stable } = checkStability(result);
    
    if (stable) {
      low = mid;
      cct = mid;
    } else {
      high = mid;
    }
  }
  
  return {
    cct,
    faultTime: 0.1,
    cctRange: [low, high]
  };
}
