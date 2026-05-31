// Power System Component Types

export interface Bus {
  id: string;
  name: string;
  type: 'slack' | 'pv' | 'pq';
  voltage: number;
  angle: number;
  vmin: number;
  vmax: number;
  area: number;
  region: number;
  x: number;
  y: number;
  active: boolean;
}

export interface Line {
  id: string;
  fromBus: string;
  toBus: string;
  resistance: number;
  reactance: number;
  susceptance: number;
  rating: number;
  active: boolean;
}

export interface Transformer {
  id: string;
  fromBus: string;
  toBus: string;
  tap: number;
  phase: number;
  impedance: number;
  active: boolean;
}

export interface Load {
  id: string;
  busId: string;
  pDemand: number;
  qDemand: number;
  active: boolean;
}

export interface Generator {
  id: string;
  busId: string;
  pGen: number;
  qGen: number;
  vSetpoint: number;
  active: boolean;
}

export interface Shunt {
  id: string;
  busId: string;
  g: number;
  b: number;
  active: boolean;
}

export interface Area {
  id: string;
  name: string;
  slackBus: string;
}

export interface PowerSystem {
  buses: Bus[];
  lines: Line[];
  transformers: Transformer[];
  loads: Load[];
  generators: Generator[];
  shunts: Shunt[];
  areas: Area[];
}

// Power Flow Results
export interface PowerFlowResult {
  converged: boolean;
  iterations: number;
  maxMismatch: number;
  slackAngle: number;
  busResults: BusResult[];
  lineResults: LineResult[];
  genResults: GeneratorResult[];
  losses: {
    real: number;
    reactive: number;
  };
}

export interface BusResult {
  id: string;
  voltage: number;
  angle: number;
  pGen: number;
  qGen: number;
  pLoad: number;
  qLoad: number;
}

export interface LineResult {
  id: string;
  pFrom: number;
  qFrom: number;
  pTo: number;
  qTo: number;
  loading: number;
}

export interface GeneratorResult {
  id: string;
  pGen: number;
  qGen: number;
  vSetpoint: number;
}

// Time Domain Simulation
export interface SimulationParams {
  tStart: number;
  tEnd: number;
  stepSize: number;
  faultLocation: string;
  faultTime: number;
  faultDuration: number;
}

export interface SimulationResult {
  time: number[];
  busVoltages: { [busId: string]: number[] };
  busAngles: { [busId: string]: number[] };
  machineAngles: { [genId: string]: number[] };
  machineSpeeds: { [genId: string]: number[] };
}

// Eigenvalue Analysis
export interface EigenvalueResult {
  eigenvalues: ComplexNumber[];
  dampingRatios: number[];
  frequencies: number[];
  modes: ModeResult[];
}

export interface ComplexNumber {
  real: number;
  imag: number;
}

export interface ModeResult {
  eigenvalue: ComplexNumber;
  frequency: number;
  dampingRatio: number;
  participationFactors: { [busId: string]: number };
}

// Settings
export interface Settings {
  baseFrequency: number;
  tolerance: number;
  maxIterations: number;
  solutionMethod: 'nr' | 'dc' | 'fast-decoupled';
  flatStart: boolean;
  beeps: boolean;
  theme: 'light' | 'dark' | 'custom';
}