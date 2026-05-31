/**
 * Power Flow Analysis Module
 * JavaScript port of PSAT power flow algorithms
 */

import { Bus, Line, PowerSystem, PowerFlowResult, BusResult, LineResult, GeneratorResult } from '@/types';

interface YBusElement {
  g: number;
  b: number;
}

interface Complex {
  real: number;
  imag: number;
}

// Complex number helpers
const complex = (real: number, imag: number = 0): Complex => ({ real, imag });
const complexAdd = (a: Complex, b: Complex): Complex => ({ real: a.real + b.real, imag: a.imag + b.imag });
const complexSub = (a: Complex, b: Complex): Complex => ({ real: a.real - b.real, imag: a.imag - b.imag });
const complexMul = (a: Complex, b: Complex): Complex => ({
  real: a.real * b.real - a.imag * b.imag,
  imag: a.real * b.imag + a.imag * b.real
});
const complexConj = (a: Complex): Complex => ({ real: a.real, imag: -a.imag });
const complexAbs = (a: Complex): number => Math.sqrt(a.real * a.real + a.imag * a.imag);
const complexFromRect = (re: number, im: number): Complex => ({ real: re, imag: im });
const complexFromPolar = (mag: number, ang: number): Complex => ({
  real: mag * Math.cos(ang),
  imag: mag * Math.sin(ang)
});

export class PowerFlowSolver {
  private system: PowerSystem;
  private Ybus: { [key: string]: { [key: string]: YBusElement } };
  private n: number;
  private busIndex: Map<string, number>;
  private indexBus: Map<number, string>;
  
  private tolerance: number = 1e-6;
  private maxIterations: number = 100;
  
  constructor(system: PowerSystem) {
    this.system = system;
    this.Ybus = {};
    this.n = system.buses.length;
    this.busIndex = new Map();
    this.indexBus = new Map();
    this.buildIndices();
  }
  
  private buildIndices(): void {
    this.system.buses.forEach((bus, idx) => {
      this.busIndex.set(bus.id, idx);
      this.indexBus.set(idx, bus.id);
    });
  }
  
  public buildYBus(): void {
    const n = this.n;
    
    // Initialize Ybus matrix
    for (let i = 0; i < n; i++) {
      this.Ybus[i] = {};
      for (let j = 0; j < n; j++) {
        this.Ybus[i][j] = { g: 0, b: 0 };
      }
    }
    
    // Add line contributions
    this.system.lines.forEach(line => {
      if (!line.active) return;
      
      const i = this.busIndex.get(line.fromBus)!;
      const j = this.busIndex.get(line.toBus)!;
      
      // Y = 1 / (R + jX)
      const z = line.resistance + line.reactance;
      const yReal = line.resistance / (z * z + line.reactance * line.reactance);
      const yImag = -line.reactance / (z * z + line.reactance * line.reactance);
      const b = line.susceptance;
      
      // Add series admittance
      this.Ybus[i][j].g += yReal;
      this.Ybus[i][j].b += yImag;
      this.Ybus[j][i].g += yReal;
      this.Ybus[j][i].b += yImag;
      
      // Add to diagonal (including half-line charging)
      this.Ybus[i][i].g += yReal;
      this.Ybus[i][i].b += yImag + b / 2;
      this.Ybus[j][j].g += yReal;
      this.Ybus[j][j].b += yImag + b / 2;
    });
    
    // Add transformer contributions
    this.system.transformers.forEach(txf => {
      if (!txf.active) return;
      
      const i = this.busIndex.get(txf.fromBus)!;
      const j = this.busIndex.get(txf.toBus)!;
      
      // Y = 1 / Z
      const z = txf.impedance;
      const yReal = 1 / z;
      const a = txf.tap > 0 ? txf.tap : 1;
      
      this.Ybus[i][j].g += yReal / a;
      this.Ybus[i][j].b += 0;
      this.Ybus[j][i].g += yReal / a;
      this.Ybus[j][i].b += 0;
      
      this.Ybus[i][i].g += yReal / a;
      this.Ybus[i][i].b += 0;
      this.Ybus[j][j].g += yReal / a;
      this.Ybus[j][j].b += 0;
    });
    
    // Add shunt contributions
    this.system.shunts.forEach(shunt => {
      if (!shunt.active) return;
      
      const i = this.busIndex.get(shunt.busId)!;
      this.Ybus[i][i].g += shunt.g;
      this.Ybus[i][i].b += shunt.b;
    });
  }
  
  public solve(): PowerFlowResult {
    this.buildYBus();
    
    const n = this.n;
    const V: Complex[] = new Array(n);
    const S: Complex[] = new Array(n);
    
    // Initialize voltages
    let slackBusIdx = -1;
    this.system.buses.forEach((bus, idx) => {
      if (bus.type === 'slack') {
        V[idx] = complex(bus.voltage, 0);
        slackBusIdx = idx;
      } else {
        V[idx] = complex(1.0, 0);
      }
      S[idx] = complex(0, 0);
    });
    
    // Build power injections from generators
    this.system.generators.forEach(gen => {
      if (!gen.active) return;
      const idx = this.busIndex.get(gen.busId);
      if (idx !== undefined) {
        S[idx] = complexAdd(S[idx], complex(gen.pGen, -gen.qGen));
      }
    });
    
    // Subtract loads from power injections
    this.system.loads.forEach(load => {
      if (!load.active) return;
      const idx = this.busIndex.get(load.busId);
      if (idx !== undefined) {
        S[idx] = complexAdd(S[idx], complex(-load.pDemand, load.qDemand));
      }
    });
    
    // Newton-Raphson Iteration
    let converged = false;
    let iterations = 0;
    let maxMismatch = 0;
    
    while (iterations < this.maxIterations) {
      // Calculate power mismatch
      const mismatch: Complex[] = new Array(n);
      maxMismatch = 0;
      
      for (let i = 0; i < n; i++) {
        let Si = complex(0, 0);
        
        for (let j = 0; j < n; j++) {
          const yij = this.Ybus[i]?.[j] || { g: 0, b: 0 };
          const yijComplex = complex(yij.g, yij.b);
          
          // Iij = Yij * Vj
          const Iij = complexMul(yijComplex, V[j]);
          
          // Si += Vi * conj(Iij)
          const ViConj = complexConj(V[i]);
          Si = complexAdd(Si, complexMul(ViConj, Iij));
        }
        
        mismatch[i] = complex(S[i].real - Si.real, S[i].imag + Si.imag);
        
        const pMismatch = Math.abs(mismatch[i].real);
        const qMismatch = Math.abs(mismatch[i].imag);
        maxMismatch = Math.max(maxMismatch, pMismatch, qMismatch);
      }
      
      if (maxMismatch < this.tolerance) {
        converged = true;
        break;
      }
      
      // Simplified update (in real implementation, this would use full Jacobian)
      for (let i = 0; i < n; i++) {
        if (this.system.buses[i].type !== 'slack') {
          const delta = mismatch[i].imag / 1.0; // Simplified gradient
          const angle = Math.atan2(V[i].imag, V[i].real) + delta * 0.1;
          const mag = complexAbs(V[i]);
          V[i] = complexFromPolar(mag, angle);
        }
      }
      
      iterations++;
    }
    
    // Calculate results
    const busResults = this.calculateBusResults(V);
    const lineResults = this.calculateLineResults(V);
    const genResults = this.calculateGenResults();
    const losses = this.calculateLosses(V);
    
    return {
      converged,
      iterations,
      maxMismatch,
      slackAngle: slackBusIdx >= 0 ? Math.atan2(V[slackBusIdx].imag, V[slackBusIdx].real) : 0,
      busResults,
      lineResults,
      genResults,
      losses
    };
  }
  
  private calculateBusResults(V: Complex[]): BusResult[] {
    return this.system.buses.map((bus, idx) => {
      const Vmag = complexAbs(V[idx]);
      const Vang = Math.atan2(V[idx].imag, V[idx].real) * 180 / Math.PI;
      
      return {
        id: bus.id,
        voltage: Vmag,
        angle: Vang,
        pGen: 0,
        qGen: 0,
        pLoad: 0,
        qLoad: 0
      };
    });
  }
  
  private calculateLineResults(V: Complex[]): LineResult[] {
    return this.system.lines.map(line => {
      const i = this.busIndex.get(line.fromBus)!;
      const j = this.busIndex.get(line.toBus)!;
      
      // Current Iij = Yij * (Vi - Vj)
      const z = line.resistance + line.reactance;
      const yMag = 1 / Math.sqrt(z * z + 0); // Simplified
      const yReal = line.resistance / (z * z);
      const yImag = -line.reactance / (z * z);
      
      const yij = complex(yReal, yImag);
      const viMinusVj = complexSub(V[i], V[j]);
      const Iij = complexMul(yij, viMinusVj);
      
      // Power Sij = Vi * conj(Iij)
      const ViConj = complexConj(V[i]);
      const Sij = complexMul(ViConj, Iij);
      
      const VjConj = complexConj(V[j]);
      const Sji = complexMul(VjConj, complexMul(complex(yReal, -yImag), viMinusVj));
      
      const loading = complexAbs(Iij) / line.rating * 100;
      
      return {
        id: line.id,
        pFrom: Sij.real,
        qFrom: -Sij.imag,
        pTo: Sji.real,
        qTo: -Sji.imag,
        loading
      };
    });
  }
  
  private calculateGenResults(): GeneratorResult[] {
    return this.system.generators.map(gen => ({
      id: gen.id,
      pGen: gen.pGen,
      qGen: gen.qGen,
      vSetpoint: gen.vSetpoint
    }));
  }
  
  private calculateLosses(V: Complex[]): { real: number; reactive: number } {
    let pLoss = 0;
    let qLoss = 0;
    
    this.system.lines.forEach(line => {
      const i = this.busIndex.get(line.fromBus)!;
      const j = this.busIndex.get(line.toBus)!;
      
      const z = line.resistance + line.reactance;
      const yMag = 1 / Math.sqrt(z * z);
      
      const viMinusVj = complexSub(V[i], V[j]);
      const IijMag = yMag * complexAbs(viMinusVj);
      
      pLoss += line.resistance * IijMag * IijMag;
      qLoss += line.reactance * IijMag * IijMag;
    });
    
    return { real: pLoss, reactive: qLoss };
  }
}

// Default system for testing
export function createDefaultSystem(): PowerSystem {
  return {
    buses: [
      { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
      { id: '2', name: 'PV1', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
      { id: '3', name: 'PQ1', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 2, y: 0, active: true },
      { id: '4', name: 'PQ2', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 3, y: 0, active: true },
    ],
    lines: [
      { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
      { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
      { id: 'L34', fromBus: '3', toBus: '4', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
    ],
    transformers: [],
    loads: [
      { id: 'LD3', busId: '3', pDemand: 1.0, qDemand: 0.5, active: true },
      { id: 'LD4', busId: '4', pDemand: 0.7, qDemand: 0.35, active: true },
    ],
    generators: [
      { id: 'G1', busId: '1', pGen: 0.8, qGen: 0, vSetpoint: 1.0, active: true },
      { id: 'G2', busId: '2', pGen: 0.5, qGen: 0, vSetpoint: 1.05, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
  };
}