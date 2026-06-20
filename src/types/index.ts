/**
 * Power System Types - Comprehensive PSAT/ETAP compatible types
 * Based on IEC/IEEE standards
 */

// ============================================================================
// Core Power System Components
// ============================================================================

export interface Bus {
  id: string;
  name: string;
  type: BusType;
  voltage: number;      // p.u.
  angle: number;         // radians
  vmin: number;         // p.u.
  vmax: number;         // p.u.
  area: number;
  region: number;
  x: number;            // Graphical position
  y: number;            // Graphical position
  active: boolean;
  // Extended properties
  vScheduled?: number;  // Scheduled voltage (p.u.)
  vbase?: number;        // Base voltage (kV)
  zone?: number;         // Loss zone
  owner?: number;        // Ownership
  comments?: string;
}

export type BusType = 'slack' | 'pv' | 'pq' | 'isolated';

export interface Line {
  id: string;
  name?: string;
  fromBus: string;
  toBus: string;
  resistance: number;    // p.u.
  reactance: number;     // p.u.
  susceptance: number;   // p.u.
  rating: number;        // MVA
  ratingA?: number;      // Emergency rating A (MVA)
  ratingB?: number;      // Emergency rating B (MVA)
  length?: number;       // km
  cost?: number;         // $/mile
  active: boolean;
  lineType?: LineType;
}

export type LineType = 'overhead' | 'underground' | 'cable' | 'tunnel';

export interface Transformer {
  id: string;
  name?: string;
  fromBus: string;
  toBus: string;
  resistance: number;    // p.u.
  reactance: number;     // p.u.
  tap: number;           // Tap position (p.u.)
  shift: number;         // Phase shift angle (degrees)
  rating: number;        // MVA
  vhigh?: number;        // High voltage (kV)
  vlow?: number;         // Low voltage (kV)
  vectorGroup?: VectorGroup;
  connection?: TransformerConnection;
  active: boolean;
}

export type VectorGroup = 'Yy0' | 'Yy6' | 'Dy1' | 'Dy11' | 'Dy5' | 'Dy7' | 'Yy4' | 'Yy8';
export type TransformerConnection = 'wye' | 'delta' | 'zigzag';

export interface Generator {
  id: string;
  name?: string;
  bus: string;
  pg: number;            // MW
  qg: number;            // MVAR
  v: number;             // p.u.
  pmax: number;          // MW
  pmin: number;          // MW
  qmax: number;          // MVAR
  qmin: number;          // MVAR
  cost?: GeneratorCost;
  model?: string;
  active: boolean;
}

export interface GeneratorCost {
  model: 'polynomial' | 'piecewise';
  c2?: number;
  c1?: number;
  c0?: number;
  startup?: number;
  shutdown?: number;
  piecewise?: { p: number; f: number }[];
}

export interface Load {
  id: string;
  name?: string;
  bus: string;
  pl: number;            // MW
  ql: number;            // MVAR
  cl?: number;
  gl?: number;
  bl?: number;
  demandModel?: DemandModel;
  active: boolean;
}

export type DemandModel = 'constant-power' | 'constant-impedance' | 'constant-current' | 'mixed';

export interface Shunt {
  id: string;
  name?: string;
  bus: string;
  g: number;
  b: number;
  vlow?: number;
  vhigh?: number;
  active: boolean;
}

export interface Area {
  id: string;
  name: string;
  slackBus: string;
}

// ============================================================================
// Complete Power System Model
// ============================================================================

export interface PowerSystem {
  buses: Bus[];
  lines: Line[];
  transformers: Transformer[];
  generators: Generator[];
  loads: Load[];
  shunts?: Shunt[];
  areas?: Area[];
  baseMVA: number;
  baseFreq: number;
  slackBus?: string;
  name?: string;
}

// ============================================================================
// Power Flow Results
// ============================================================================

export interface BusResult {
  bus: string;
  v: number;
  angle: number;
  pg: number;
  qg: number;
  pl: number;
  ql: number;
  qshunt: number;
}

export interface LineResult {
  line: string;
  fromBus: string;
  toBus: string;
  pFrom: number;
  qFrom: number;
  pTo: number;
  qTo: number;
  ploss: number;
  qloss: number;
  loading: number;
}

export interface TransformerResult {
  transformer: string;
  fromBus: string;
  toBus: string;
  pFrom: number;
  qFrom: number;
  pTo: number;
  qTo: number;
  loading: number;
  tap: number;
}

export interface GeneratorResult {
  generator: string;
  bus: string;
  pg: number;
  qg: number;
  v: number;
  status: 'on' | 'off' | 'at limit';
}

export interface PowerFlowResult {
  converged: boolean;
  iterations: number;
  maxMismatch: number;
  losses: { real: number; imag: number };
  busResults: BusResult[];
  lineResults: LineResult[];
  transformerResults?: TransformerResult[];
  generatorResults: GeneratorResult[];
  elapsedTime: number;
  method: PowerFlowMethod;
}

export type PowerFlowMethod = 'Newton-Raphson' | 'Fast-Decoupled' | 'DC' | 'Gauss-Seidel' | 'HOLAR' | 'Hybrid';

// ============================================================================
// Time Domain Simulation
// ============================================================================

export interface SimulationParams {
  tStart: number;
  tEnd: number;
  stepSize: number;
  faultLocation?: string;
  faultTime?: number;
  faultDuration?: number;
}

export interface SimulationResult {
  time: number[];
  busVoltages: { [busId: string]: number[] };
  busAngles: { [busId: string]: number[] };
  machineAngles: { [genId: string]: number[] };
  machineSpeeds: { [genId: string]: number[] };
  events?: SimulationEvent[];
  elapsedTime: number;
}

export interface SimulationEvent {
  time: number;
  type: string;
  element: string;
  description: string;
}

// ============================================================================
// Eigenvalue Analysis
// ============================================================================

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

// ============================================================================
// Settings
// ============================================================================

export interface Settings {
  baseFrequency: number;
  tolerance: number;
  maxIterations: number;
  solutionMethod: 'nr' | 'dc' | 'fast-decoupled';
  flatStart: boolean;
  beeps: boolean;
  theme: 'light' | 'dark' | 'custom';
}

// ============================================================================
// IEC Symbol Types
// ============================================================================

export type IECSymbolType = 
  | 'bus'
  | 'generator'
  | 'load'
  | 'motor'
  | 'shunt'
  | 'capacitor'
  | 'reactor'
  | 'capacitor-bank'
  | 'reactor-bank'
  | 'busbar'
  | 'line'
  | 'transformer'
  | 'transformer-3w'
  | 'transformer-reg'
  | 'breaker'
  | 'switch'
  | 'disconnect'
  | 'fuse'
  | 'sectionalizer'
  | 'recloser'
  | 'current-transformer'
  | 'potential-transformer'
  | 'relay'
  | 'meter'
  | 'ground'
  | 'external-grid'
  | 'equivalent'
  | 'svc'
  | 'statcom'
  | 'tcsc'
  | 'upfc'
  | 'wind-turbine'
  | 'pv-array'
  | 'battery'
  | 'substation'
  | 'consortium'
  | 'arrestor'
  | 'junction';

export interface IECSymbol {
  type: IECSymbolType;
  name: string;
  ieeeSymbol?: string;
  category: IECSymbolCategory;
  subcategory?: string;
  width: number;
  height: number;
  connectionPoints: ConnectionPoint[];
  properties: ComponentProperty[];
  render: (ctx: CanvasRenderingContext2D, x: number, y: number, rotation?: number) => void;
}

export type IECSymbolCategory = 
  | 'generation'
  | 'load'
  | 'transmission'
  | 'distribution'
  | 'protection'
  | 'measurement'
  | 'compensation'
  | 'storage'
  | 'renewable'
  | 'substation'
  | 'network';

export interface ConnectionPoint {
  id: string;
  x: number;
  y: number;
  type: 'top' | 'bottom' | 'left' | 'right' | 'any';
  busId?: string;
}

export interface ComponentProperty {
  key: string;
  label: string;
  type: 'number' | 'string' | 'boolean' | 'select' | 'readonly';
  unit?: string;
  default?: any;
  min?: number;
  max?: number;
  step?: number;
  options?: { value: string; label: string }[];
  category?: string;
  description?: string;
}
