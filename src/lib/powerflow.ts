import { PowerSystem, PowerFlowResult } from '@/types';
import { solveLU } from './matrix';
import { Complex, cAbs, cAngle, cPolar, cDeg } from './complex';
import {
  buildYBus, getIndices, getScheduledPower, initializeV,
  buildFullJacobian, buildMismatchVector, doNRStep,
  calcBusResults, calcLineResults, calcLosses, solveNR,
  YBusMatrix, SystemIndices
} from './solver-core';

export interface SolverConfig {
  tolerance: number;
  maxIterations: number;
  flatStart: boolean;
}

export function buildYBusPublic(system: PowerSystem): { Y: YBusMatrix; n: number; busIndex: Map<string, number> } {
  const { Y, busIndex } = buildYBus(system);
  return { Y, n: system.buses.length, busIndex };
}

export class PowerFlowSolver {
  private system: PowerSystem;
  private Y: YBusMatrix;
  private indices: SystemIndices;
  private busIndex: Map<string, number>;

  constructor(system: PowerSystem, config?: Partial<SolverConfig>) {
    this.system = system;
    const yRes = buildYBus(system);
    this.Y = yRes.Y;
    this.indices = getIndices(system);
    this.busIndex = yRes.busIndex;
  }

  solve(method?: 'nr' | 'dc' | 'fast-decoupled'): PowerFlowResult {
    switch (method || 'nr') {
      case 'dc': return this.solveDC();
      case 'fast-decoupled': return this.solveFastDecoupled();
      default: return this.solveNR();
    }
  }

  private solveNR(): PowerFlowResult {
    const { system, Y, indices, busIndex } = this;
    const V = initializeV(system, true);
    const { Psp, Qsp } = getScheduledPower(system, busIndex);

    const result = solveNR(V, Psp, Qsp, Y, indices, 100, 1e-8);
    const slackV = indices.slackIdx >= 0 ? V[indices.slackIdx] : null;

    return {
      converged: result.converged,
      iterations: result.iterations,
      maxMismatch: result.maxMismatch,
      slackAngle: slackV ? cDeg(slackV) : 0,
      busResults: calcBusResults(system, V, busIndex),
      lineResults: calcLineResults(system, V, busIndex),
      genResults: system.generators.filter(g => g.active).map(gen => ({
        id: gen.id,
        pGen: gen.pGen,
        qGen: gen.qGen,
        vSetpoint: busIndex.has(gen.busId) ? cAbs(V[busIndex.get(gen.busId)!]) : gen.vSetpoint,
      })),
      losses: calcLosses(system, V, busIndex),
    };
  }

  private solveDC(): PowerFlowResult {
    const { system, indices, busIndex } = this;
    const { n, slackIdx, thetaMap, ntheta } = indices;
    const B = Array.from({ length: ntheta }, () => new Array(ntheta).fill(0));
    const Psp = new Array(ntheta).fill(0);

    const thetaPos = new Array(n).fill(-1);
    thetaMap.forEach((v, i) => { thetaPos[v] = i; });

    system.lines.forEach(line => {
      if (!line.active) return;
      const fi = busIndex.get(line.fromBus)!, ti = busIndex.get(line.toBus)!;
      const x = line.reactance;
      if (x === 0) return;
      const bSus = -1 / x;
      const fp = thetaPos[fi], tp = thetaPos[ti];
      if (fp >= 0) { B[fp][fp] += bSus; Psp[fp] += busPInjection(system, busIndex, fi); }
      if (tp >= 0) { B[tp][tp] += bSus; Psp[tp] += busPInjection(system, busIndex, ti); }
      if (fp >= 0 && tp >= 0) { B[fp][tp] -= bSus; B[tp][fp] -= bSus; }
    });

    system.transformers.forEach(txf => {
      if (!txf.active) return;
      const fi = busIndex.get(txf.fromBus)!, ti = busIndex.get(txf.toBus)!;
      const x = txf.impedance;
      if (x === 0) return;
      const tap = txf.tap > 0 ? txf.tap : 1;
      const bSus = -1 / x;
      const fp = thetaPos[fi], tp = thetaPos[ti];
      if (fp >= 0) B[fp][fp] += bSus / (tap * tap);
      if (tp >= 0) B[tp][tp] += bSus;
      if (fp >= 0 && tp >= 0) { B[fp][tp] -= bSus / tap; B[tp][fp] -= bSus / tap; }
    });

    let theta: number[];
    try { theta = solveLU(B, Psp); } catch {
      return { converged: false, iterations: 0, maxMismatch: Infinity, slackAngle: 0, busResults: [], lineResults: [], genResults: [], losses: { real: 0, reactive: 0 } };
    }

    const V: Complex[] = new Array(n);
    system.buses.forEach((bus, i) => {
      const ang = i === slackIdx ? 0 : theta[thetaPos[i]];
      V[i] = cPolar(bus.type === 'slack' ? bus.voltage : 1.0, ang);
    });

    return {
      converged: true, iterations: 0, maxMismatch: 0, slackAngle: 0,
      busResults: calcBusResults(system, V, busIndex),
      lineResults: calcLineResults(system, V, busIndex),
      genResults: system.generators.filter(g => g.active).map(g => ({ id: g.id, pGen: g.pGen, qGen: g.qGen, vSetpoint: g.vSetpoint })),
      losses: { real: 0, reactive: 0 },
    };
  }

  private solveFastDecoupled(): PowerFlowResult {
    const { system, Y, indices, busIndex } = this;
    const { n, slackIdx, pvIndices, pqIndices, thetaMap, ntheta, npq } = indices;
    const V = initializeV(system, true);
    const { Psp, Qsp } = getScheduledPower(system, busIndex);
    const maxIter = 100;
    const tol = 1e-8;

    const B1 = Array.from({ length: ntheta }, () => new Array(ntheta).fill(0));
    const B2 = Array.from({ length: npq }, () => new Array(npq).fill(0));
    const thetaPos = new Array(n).fill(-1);
    thetaMap.forEach((v, i) => { thetaPos[v] = i; });

    const addSus = (fi: number, ti: number, bSus: number) => {
      const fp = thetaPos[fi], tp = thetaPos[ti];
      if (fp >= 0) B1[fp][fp] -= bSus;
      if (tp >= 0) B1[tp][tp] -= bSus;
      if (fp >= 0 && tp >= 0) { B1[fp][tp] += bSus; B1[tp][fp] += bSus; }
      const fq = pqIndices.indexOf(fi), tq = pqIndices.indexOf(ti);
      if (fq >= 0) B2[fq][fq] -= bSus;
      if (tq >= 0) B2[tq][tq] -= bSus;
      if (fq >= 0 && tq >= 0) { B2[fq][tq] += bSus; B2[tq][fq] += bSus; }
    };

    system.lines.forEach(line => {
      if (!line.active) return;
      const fi = busIndex.get(line.fromBus)!, ti = busIndex.get(line.toBus)!;
      if (line.reactance === 0) return;
      addSus(fi, ti, -1 / line.reactance);
    });
    system.transformers.forEach(txf => {
      if (!txf.active) return;
      const fi = busIndex.get(txf.fromBus)!, ti = busIndex.get(txf.toBus)!;
      if (txf.impedance === 0) return;
      addSus(fi, ti, -1 / txf.impedance);
    });

    let converged = false, iterations = 0;

    while (iterations < maxIter) {
      const { Pcalc, Qcalc } = calcAllPQI_sync(V, Y);
      let maxMis = 0;
      const dP: number[] = [];
      for (let ii = 0; ii < ntheta; ii++) {
        const i = thetaMap[ii];
        dP.push(Psp[i] - Pcalc[i]);
        maxMis = Math.max(maxMis, Math.abs(dP[ii]));
      }
      const dQ: number[] = [];
      pqIndices.forEach(i => {
        dQ.push(Qsp[i] + Qcalc[i]);
        maxMis = Math.max(maxMis, Math.abs(dQ[dQ.length - 1]));
      });

      if (maxMis < tol) { converged = true; break; }

      try {
        const dTheta = solveLU(B1, dP);
        thetaMap.forEach((i, ii) => { V[i] = cPolar(cAbs(V[i]), cAngle(V[i]) + dTheta[ii]); });
        const qNorm = dQ.map((v, qi) => v / cAbs(V[pqIndices[qi]]));
        const dVolt = solveLU(B2, qNorm);
        pqIndices.forEach((i, qi) => { V[i] = cPolar(cAbs(V[i]) * (1 + dVolt[qi]), cAngle(V[i])); });
        pvIndices.forEach(i => { V[i] = cPolar(system.buses[i].voltage, cAngle(V[i])); });
        if (slackIdx >= 0) V[slackIdx] = cPolar(cAbs(V[slackIdx]), 0);
      } catch { break; }

      iterations++;
    }

    const slackV = slackIdx >= 0 ? V[slackIdx] : null;
    return {
      converged, iterations,
      maxMismatch: converged ? 0 : maxIter,
      slackAngle: slackV ? cDeg(slackV) : 0,
      busResults: calcBusResults(system, V, busIndex),
      lineResults: calcLineResults(system, V, busIndex),
      genResults: system.generators.filter(g => g.active).map(g => ({ id: g.id, pGen: g.pGen, qGen: g.qGen, vSetpoint: cAbs(V[busIndex.get(g.busId)!]) })),
      losses: calcLosses(system, V, busIndex),
    };
  }

  getYBusMatrix(): { g: number; b: number }[][] {
    const n = this.system.buses.length;
    const m: { g: number; b: number }[][] = [];
    for (let i = 0; i < n; i++) {
      m[i] = [];
      for (let j = 0; j < n; j++) {
        m[i][j] = this.Y[i]?.[j] || { g: 0, b: 0 };
      }
    }
    return m;
  }
}

function calcAllPQI_sync(V: Complex[], Y: any): { Pcalc: number[]; Qcalc: number[] } {
  const n = V.length;
  const Pcalc = new Array(n).fill(0);
  const Qcalc = new Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    let p = 0, q = 0;
    for (let j = 0; j < n; j++) {
      const y = Y[i]?.[j] || { g: 0, b: 0 };
      const theta = cAngle(V[i]) - cAngle(V[j]);
      const vv = cAbs(V[i]) * cAbs(V[j]);
      p += vv * (y.g * Math.cos(theta) + y.b * Math.sin(theta));
      q += vv * (y.g * Math.sin(theta) - y.b * Math.cos(theta));
    }
    Pcalc[i] = p; Qcalc[i] = q;
  }
  return { Pcalc, Qcalc };
}

function busPInjection(system: PowerSystem, busIndex: Map<string, number>, idx: number): number {
  let p = 0;
  system.generators.forEach(g => { if (g.active && busIndex.get(g.busId) === idx) p += g.pGen; });
  system.loads.forEach(l => { if (l.active && busIndex.get(l.busId) === idx) p -= l.pDemand; });
  return p;
}

export function createDefaultSystem(): PowerSystem {
  return {
    buses: [
      { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
      { id: '2', name: 'PV1', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1.5, y: 0, active: true },
      { id: '3', name: 'PQ1', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 3, y: 0, active: true },
      { id: '4', name: 'PQ2', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 4.5, y: 0, active: true },
    ],
    lines: [
      { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0.02, rating: 100, active: true },
      { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.015, reactance: 0.03, susceptance: 0.015, rating: 80, active: true },
      { id: 'L34', fromBus: '3', toBus: '4', resistance: 0.02, reactance: 0.04, susceptance: 0.02, rating: 60, active: true },
    ],
    transformers: [],
    loads: [
      { id: 'LD3', busId: '3', pDemand: 1.2, qDemand: 0.6, active: true },
      { id: 'LD4', busId: '4', pDemand: 0.8, qDemand: 0.4, active: true },
    ],
    generators: [
      { id: 'G1', busId: '1', pGen: 2.0, qGen: 0, vSetpoint: 1.0, active: true },
      { id: 'G2', busId: '2', pGen: 0.5, qGen: 0, vSetpoint: 1.05, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
  };
}
