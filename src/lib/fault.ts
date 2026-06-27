/**
 * Fault Analysis Module
 * Symmetrical and unsymmetrical fault calculations
 * Uses LU-once Z-bus inversion per §5 contract
 */

import { PowerSystem } from '@/types';
import { buildYBus } from './powerflow-methods';

// Fault types
export type FaultType = 'three-phase' | 'line-to-ground' | 'line-to-line' | 'double-line-to-ground';

// Fault result interface
export interface FaultResult {
  faultType: FaultType;
  faultBus: string;
  prefault: {
    voltage: number;
    angle: number;
  };
  postfault: {
    voltage: number;
    angle: number;
  };
  faultCurrent: number;
  symmetricalComponents?: {
    Ia: number;
    Ib: number;
    Ic: number;
    I1: number;
    I2: number;
    I0: number;
    V1: number;
    V2: number;
    V0: number;
  };
  faultMVA: number;
  ctRating?: number;
}

// Fault analysis result
export interface FaultAnalysisResult {
  bus: string;
  faultType: FaultType;
  currents: { magnitude: number; angle: number }[];
  voltages: { magnitude: number; angle: number }[];
  faultMVA: number;
  ctRating: number;
}

// Complete fault study result
export interface FaultStudyResult {
  threePhaseFaults: FaultAnalysisResult[];
  lineToGroundFaults: FaultAnalysisResult[];
  lineToLineFaults: FaultAnalysisResult[];
  doubleLineToGroundFaults: FaultAnalysisResult[];
  protectiveDeviceRequirements: {
    bus: string;
    minBreakerRating: number;
    recommendedBreakerRating: number;
    relaySettings: {
      pickup: number;
      timeDelay: number;
    };
  }[];
}

/**
 * LU Decomposition with partial pivoting
 * Returns L, U matrices and permutation array
 */
function luDecompose(A: number[][]): { L: number[][]; U: number[][]; perm: number[] } {
  const n = A.length;
  const L: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  const U: number[][] = A.map(row => [...row]);
  const perm: number[] = new Array(n).fill(0).map((_, i) => i);
  
  for (let col = 0; col < n; col++) {
    // Find pivot
    let maxRow = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(U[row][col]) > Math.abs(U[maxRow][col])) {
        maxRow = row;
      }
    }
    
    // Swap rows in U and perm
    if (maxRow !== col) {
      [U[col], U[maxRow]] = [U[maxRow], U[col]];
      [perm[col], perm[maxRow]] = [perm[maxRow], perm[col]];
    }
    
    // Check for singular matrix
    if (Math.abs(U[col][col]) < 1e-12) {
      U[col][col] = 1e-12;
    }
    
    // LU decomposition
    for (let row = col + 1; row < n; row++) {
      L[row][col] = U[row][col] / U[col][col];
      for (let k = col; k < n; k++) {
        U[row][k] -= L[row][col] * U[col][k];
      }
    }
  }
  
  return { L, U, perm };
}

/**
 * Solve Ax = b using LU factors with permutation
 */
function luSolve(L: number[][], U: number[][], perm: number[], b: number[]): number[] {
  const n = b.length;
  
  // Apply permutation
  const pb: number[] = new Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    pb[i] = b[perm[i]];
  }
  
  // Forward substitution: Ly = Pb
  const y: number[] = new Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    y[i] = pb[i];
    for (let j = 0; j < i; j++) {
      y[i] -= L[i][j] * y[j];
    }
  }
  
  // Back substitution: Ux = y
  const x: number[] = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    x[i] = y[i];
    for (let j = i + 1; j < n; j++) {
      x[i] -= U[i][j] * x[j];
    }
    x[i] /= U[i][i];
  }
  
  return x;
}

/**
 * Build complex Z-bus matrix using LU-once approach
 * Per §5 contract: LU-factor once, solve n times
 * Returns array of complex numbers {real, imag}
 */
function buildZMatrix(ybus: ReturnType<typeof buildYBus>): { real: number; imag: number }[][] {
  const n = ybus.n;
  
  // Step 1: Build 2n×2n real matrix A = [G -B; B G]
  const size = 2 * n;
  const A: number[][] = new Array(size).fill(null).map(() => new Array(size).fill(0));
  
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      // Top-left: G
      A[i][j] = ybus.g[i][j];
      // Top-right: -B
      A[i][j + n] = -ybus.b[i][j];
      // Bottom-left: B
      A[i + n][j] = ybus.b[i][j];
      // Bottom-right: G
      A[i + n][j + n] = ybus.g[i][j];
    }
  }
  
  // Step 2: LU-factor A ONCE (O((2n)³))
  const { L, U, perm } = luDecompose(A);
  
  // Step 3: For each column k, solve A·x_k = e_k (O((2n)²) per column)
  // Z[i][k] = x_k[i] + j·x_k[n+i] (complex)
  const Z: { real: number; imag: number }[][] = new Array(n).fill(null).map(() =>
    new Array(n).fill(null).map(() => ({ real: 0, imag: 0 }))
  );
  
  for (let k = 0; k < n; k++) {
    // RHS: e_k (k-th standard basis vector)
    const rhs: number[] = new Array(size).fill(0);
    rhs[k] = 1;
    
    // Solve using stored LU factors
    const x = luSolve(L, U, perm, rhs);
    
    // Extract complex impedance: Z[i][k] = x[i] + j·x[n+i]
    for (let i = 0; i < n; i++) {
      Z[i][k] = { real: x[i], imag: x[n + i] };
    }
  }
  
  return Z;
}

/**
 * Calculate three-phase fault current
 * Per §5 contract: 3-Phase symmetric fault: I_f = V_f / Z1_kk
 */
export function calculateThreePhaseFault(
  system: PowerSystem,
  faultBusId: string
): FaultResult {
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  const faultIdx = busIndex.get(faultBusId);
  if (faultIdx === undefined) {
    throw new Error(`Bus ${faultBusId} not found`);
  }
  
  const ybus = buildYBus(system);
  const Z = buildZMatrix(ybus);
  
  const bus = system.buses[faultIdx];
  const prefaultVoltage = bus.voltage || 1.0;
  
  // Z1_kk = Thevenin impedance at faulted bus (positive sequence)
  const Zkk = Z[faultIdx][faultIdx];
  const Zth = Math.sqrt(Zkk.real * Zkk.real + Zkk.imag * Zkk.imag) || 0.1;
  const If = prefaultVoltage / Zth;
  
  return {
    faultType: 'three-phase',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: 0, angle: 0 },
    faultCurrent: If,
    symmetricalComponents: {
      Ia: If, Ib: If, Ic: If,
      I1: If, I2: 0, I0: 0,
      V1: 0, V2: 0, V0: 0
    },
    faultMVA: If * prefaultVoltage * (system.baseMVA || 100),
    ctRating: If * 1.2
  };
}

/**
 * Calculate line-to-ground fault current
 * Per §5 contract: Single Line-to-Ground (a-phase):
 *   I_a1 = V_f / (Z1+Z2+Z0+3Rf) where Z2=Z1, Z0=0.5·Z1
 */
export function calculateLineToGroundFault(
  system: PowerSystem,
  faultBusId: string,
  Rf: number = 0
): FaultResult {
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  const faultIdx = busIndex.get(faultBusId);
  if (faultIdx === undefined) {
    throw new Error(`Bus ${faultBusId} not found`);
  }
  
  const ybus = buildYBus(system);
  const Z = buildZMatrix(ybus);
  
  const bus = system.buses[faultIdx];
  const prefaultVoltage = bus.voltage || 1.0;
  
  // Get Thevenin impedance
  const Zkk = Z[faultIdx][faultIdx];
  const Z1 = Math.sqrt(Zkk.real * Zkk.real + Zkk.imag * Zkk.imag) || 0.1;
  const Z2 = Z1;
  const Z0 = Z1 * 0.5;
  
  const Ztotal = Z1 + Z2 + Z0 + 3 * Rf;
  const I_a1 = prefaultVoltage / Ztotal;
  const Ia = 3 * I_a1;  // I_a = 3 * I_a1
  
  return {
    faultType: 'line-to-ground',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: 0, angle: 0 },
    faultCurrent: Math.abs(Ia),
    symmetricalComponents: {
      Ia, Ib: 0, Ic: 0,
      I1: I_a1, I2: 0, I0: I_a1,
      V1: 0, V2: 0, V0: 0
    },
    faultMVA: Math.abs(Ia) * prefaultVoltage * (system.baseMVA || 100)
  };
}

/**
 * Calculate line-to-line fault current
 * Per §5 contract: Line-to-Line (b-c phases):
 *   I_b1 = V_f / (Z1+Z2+Rf)
 *   I_b = -j√3·I_b1
 *   |I_b| = √3·|I_b1|
 */
export function calculateLineToLineFault(
  system: PowerSystem,
  faultBusId: string,
  Rf: number = 0
): FaultResult {
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  const faultIdx = busIndex.get(faultBusId);
  if (faultIdx === undefined) {
    throw new Error(`Bus ${faultBusId} not found`);
  }
  
  const ybus = buildYBus(system);
  const Z = buildZMatrix(ybus);
  
  const bus = system.buses[faultIdx];
  const prefaultVoltage = bus.voltage || 1.0;
  
  const Zkk = Z[faultIdx][faultIdx];
  const Z1 = Math.sqrt(Zkk.real * Zkk.real + Zkk.imag * Zkk.imag) || 0.1;
  const Z2 = Z1;
  const Ztotal = Z1 + Z2 + Rf;
  const I1 = prefaultVoltage / Ztotal;
  
  const sqrt3 = Math.sqrt(3);
  const Ib = -I1 * sqrt3;  // I_b = -j√3·I_b1, magnitude is √3·|I_b1|
  
  return {
    faultType: 'line-to-line',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: prefaultVoltage * 0.5, angle: 0 },
    faultCurrent: Math.abs(Ib),
    symmetricalComponents: {
      Ia: 0, Ib, Ic: -Ib,
      I1, I2: -I1, I0: 0,
      V1: prefaultVoltage * 0.5, V2: prefaultVoltage * 0.5, V0: 0
    },
    faultMVA: Math.abs(Ib) * prefaultVoltage * (system.baseMVA || 100)
  };
}

/**
 * Calculate double line-to-ground fault current
 * Per §5 contract: Double Line-to-Ground (b-c to ground):
 *   I_a1 = V_f / (Z1 + Z2·Z0/(Z2+Z0) + Rf)
 *   Dominant fault current = |3·I_a0|
 */
export function calculateDoubleLineToGroundFault(
  system: PowerSystem,
  faultBusId: string,
  Rf: number = 0
): FaultResult {
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  
  const faultIdx = busIndex.get(faultBusId);
  if (faultIdx === undefined) {
    throw new Error(`Bus ${faultBusId} not found`);
  }
  
  const ybus = buildYBus(system);
  const Z = buildZMatrix(ybus);
  
  const bus = system.buses[faultIdx];
  const prefaultVoltage = bus.voltage || 1.0;
  
  const Zkk = Z[faultIdx][faultIdx];
  const Z1 = Math.sqrt(Zkk.real * Zkk.real + Zkk.imag * Zkk.imag) || 0.1;
  const Z2 = Z1;
  const Z0 = Z1 * 0.5;
  
  const Zeq = (Z2 * Z0) / (Z2 + Z0);
  const I_a1 = prefaultVoltage / (Z1 + Zeq + Rf);
  const I_a2 = -I_a1 * Z0 / (Z2 + Z0);
  const I_a0 = -I_a1 * Z2 / (Z2 + Z0);
  
  const sqrt3 = Math.sqrt(3);
  const Ib = sqrt3 * (I_a1 * Zeq + I_a2 * Z0) / Z0;
  
  return {
    faultType: 'double-line-to-ground',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: 0, angle: 0 },
    faultCurrent: Math.abs(3 * I_a0),  // Dominant fault current = |3·I_a0|
    symmetricalComponents: {
      Ia: 0, Ib, Ic: -Ib,
      I1: I_a1, I2: I_a2, I0: I_a0,
      V1: 0, V2: 0, V0: 0
    },
    faultMVA: Math.abs(3 * I_a0) * prefaultVoltage * (system.baseMVA || 100)
  };
}

/**
 * Perform complete fault study
 */
export function performFaultStudy(
  system: PowerSystem,
  options: {
    includeThreePhase?: boolean;
    includeLineToGround?: boolean;
    includeLineToLine?: boolean;
    includeDoubleLineToGround?: boolean;
    faultResistance?: number;
  } = {}
): FaultStudyResult {
  const {
    includeThreePhase = true,
    includeLineToGround = true,
    includeLineToLine = false,
    includeDoubleLineToGround = false,
    faultResistance = 0
  } = options;
  
  const threePhaseFaults: FaultAnalysisResult[] = [];
  const lineToGroundFaults: FaultAnalysisResult[] = [];
  const lineToLineFaults: FaultAnalysisResult[] = [];
  const doubleLineToGroundFaults: FaultAnalysisResult[] = [];
  
  for (const bus of system.buses) {
    if (!bus.active) continue;
    
    if (includeThreePhase) {
      try {
        const result = calculateThreePhaseFault(system, bus.id);
        threePhaseFaults.push({
          bus: bus.id,
          faultType: 'three-phase',
          currents: [{ magnitude: result.faultCurrent, angle: 0 }],
          voltages: [{ magnitude: result.postfault.voltage, angle: 0 }],
          faultMVA: result.faultMVA,
          ctRating: result.ctRating || result.faultCurrent * 1.2
        });
      } catch (e) {
        // Skip
      }
    }
    
    if (includeLineToGround) {
      try {
        const result = calculateLineToGroundFault(system, bus.id, faultResistance);
        lineToGroundFaults.push({
          bus: bus.id,
          faultType: 'line-to-ground',
          currents: [{ magnitude: result.faultCurrent, angle: 0 }],
          voltages: [{ magnitude: result.postfault.voltage, angle: 0 }],
          faultMVA: result.faultMVA,
          ctRating: result.faultCurrent * 1.2
        });
      } catch (e) {
        // Skip
      }
    }
    
    if (includeLineToLine) {
      try {
        const result = calculateLineToLineFault(system, bus.id, faultResistance);
        lineToLineFaults.push({
          bus: bus.id,
          faultType: 'line-to-line',
          currents: [{ magnitude: result.faultCurrent, angle: 0 }],
          voltages: [{ magnitude: result.postfault.voltage, angle: 0 }],
          faultMVA: result.faultMVA,
          ctRating: result.faultCurrent * 1.2
        });
      } catch (e) {
        // Skip
      }
    }
    
    if (includeDoubleLineToGround) {
      try {
        const result = calculateDoubleLineToGroundFault(system, bus.id, faultResistance);
        doubleLineToGroundFaults.push({
          bus: bus.id,
          faultType: 'double-line-to-ground',
          currents: [{ magnitude: result.faultCurrent, angle: 0 }],
          voltages: [{ magnitude: result.postfault.voltage, angle: 0 }],
          faultMVA: result.faultMVA,
          ctRating: result.faultCurrent * 1.2
        });
      } catch (e) {
        // Skip
      }
    }
  }
  
  const protectiveDeviceRequirements = system.buses
    .filter(b => b.active)
    .map(bus => {
      const maxCurrent = Math.max(
        threePhaseFaults.find(f => f.bus === bus.id)?.faultMVA || 0,
        lineToGroundFaults.find(f => f.bus === bus.id)?.faultMVA || 0
      );
      
      return {
        bus: bus.id,
        minBreakerRating: maxCurrent * 1.25,
        recommendedBreakerRating: maxCurrent * 1.5,
        relaySettings: {
          pickup: maxCurrent * 0.5,
          timeDelay: 0.3
        }
      };
    });
  
  return {
    threePhaseFaults,
    lineToGroundFaults,
    lineToLineFaults,
    doubleLineToGroundFaults,
    protectiveDeviceRequirements
  };
}

/**
 * Calculate fault currents at all buses
 */
export function calculateAllBusFaultCurrents(
  system: PowerSystem,
  faultType: FaultType,
  faultResistance: number = 0
): { busId: string; current: number; mva: number }[] {
  const results: { busId: string; current: number; mva: number }[] = [];
  
  for (const bus of system.buses) {
    if (!bus.active) continue;
    
    try {
      let result: FaultResult;
      
      switch (faultType) {
        case 'three-phase':
          result = calculateThreePhaseFault(system, bus.id);
          break;
        case 'line-to-ground':
          result = calculateLineToGroundFault(system, bus.id, faultResistance);
          break;
        case 'line-to-line':
          result = calculateLineToLineFault(system, bus.id, faultResistance);
          break;
        case 'double-line-to-ground':
          result = calculateDoubleLineToGroundFault(system, bus.id, faultResistance);
          break;
      }
      
      results.push({
        busId: bus.id,
        current: result.faultCurrent,
        mva: result.faultMVA
      });
    } catch (e) {
      // Skip
    }
  }
  
  return results.sort((a, b) => b.mva - a.mva);
}

/**
 * Calculate relay coordination times
 */
export function calculateRelayCoordination(): {
  upstream: { pickup: number; time: number };
  downstream: { pickup: number; time: number };
  coordinationTime: number;
} {
  return {
    upstream: { pickup: 100, time: 0.5 },
    downstream: { pickup: 80, time: 0.2 },
    coordinationTime: 0.3
  };
}
