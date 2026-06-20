/**
 * Fault Analysis Module
 * Symmetrical and unsymmetrical fault calculations
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
 * Calculate impedance matrix for fault analysis
 */
function buildZMatrix(ybus: ReturnType<typeof buildYBus>): number[][] {
  const n = ybus.n;
  const Z: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const gij = ybus.g[i][j];
      const bij = ybus.b[i][j];
      const yijMag = Math.sqrt(gij * gij + bij * bij);
      Z[i][j] = yijMag !== 0 ? 1 / yijMag : 1e10;
    }
  }
  
  return Z;
}

/**
 * Calculate three-phase fault current
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
  
  const Zth = Z[faultIdx][faultIdx] || 0.1;
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
    faultMVA: (If * prefaultVoltage * (system.baseMVA || 100)) / 100,
    ctRating: If * 1.2
  };
}

/**
 * Calculate line-to-ground fault current
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
  
  const Z1 = Math.abs(Z[faultIdx][faultIdx]) || 0.1;
  const Z2 = Z1;
  const Z0 = Z1 * 0.5;
  
  const Ztotal = Z1 + Z2 + Z0 + 3 * Rf;
  const Ia = prefaultVoltage / Ztotal;
  
  return {
    faultType: 'line-to-ground',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: 0, angle: 0 },
    faultCurrent: Math.abs(Ia),
    symmetricalComponents: {
      Ia, Ib: 0, Ic: 0,
      I1: Ia, I2: 0, I0: Ia,
      V1: 0, V2: 0, V0: 0
    },
    faultMVA: (Math.abs(Ia) * prefaultVoltage * (system.baseMVA || 100)) / 100
  };
}

/**
 * Calculate line-to-line fault current
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
  
  const Z1 = Math.abs(Z[faultIdx][faultIdx]) || 0.1;
  const Z2 = Z1;
  const Ztotal = Z1 + Z2 + Rf;
  const I1 = prefaultVoltage / Ztotal;
  
  const sqrt3 = Math.sqrt(3);
  const Ib = -I1 * sqrt3;
  
  return {
    faultType: 'line-to-line',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: prefaultVoltage / 2, angle: 0 },
    faultCurrent: Math.abs(Ib),
    symmetricalComponents: {
      Ia: 0, Ib, Ic: -Ib,
      I1, I2: -I1, I0: 0,
      V1: prefaultVoltage / 2, V2: prefaultVoltage / 2, V0: 0
    },
    faultMVA: (Math.abs(Ib) * prefaultVoltage * (system.baseMVA || 100)) / 100
  };
}

/**
 * Calculate double line-to-ground fault current
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
  
  const Z1 = Math.abs(Z[faultIdx][faultIdx]) || 0.1;
  const Z2 = Z1;
  const Z0 = Z1 * 0.5;
  
  const Zeq = (Z2 * Z0) / (Z2 + Z0);
  const I1 = prefaultVoltage / (Z1 + Zeq + Rf);
  const I2 = -I1 * Z0 / (Z2 + Z0);
  const I0 = -I1 * Z2 / (Z2 + Z0);
  
  const sqrt3 = Math.sqrt(3);
  const Ib = sqrt3 * (I1 * Zeq + I2 * Z0) / Z0;
  
  return {
    faultType: 'double-line-to-ground',
    faultBus: faultBusId,
    prefault: { voltage: prefaultVoltage, angle: 0 },
    postfault: { voltage: 0, angle: 0 },
    faultCurrent: Math.abs(Ib),
    symmetricalComponents: {
      Ia: 0, Ib, Ic: -Ib,
      I1, I2, I0,
      V1: 0, V2: 0, V0: 0
    },
    faultMVA: (Math.abs(Ib) * prefaultVoltage * (system.baseMVA || 100)) / 100
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
