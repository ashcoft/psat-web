import { PowerSystem, Bus, Line } from '@/types';
import { Complex, cAbs, cAngle, cPolar, cDeg } from './complex';
import { solveLU } from './matrix';

export interface YBusElement { g: number; b: number }
export type YBusMatrix = { [row: number]: { [col: number]: YBusElement } };

export interface SystemIndices {
  n: number;
  slackIdx: number;
  pvIndices: number[];
  pqIndices: number[];
  thetaMap: number[];
  ntheta: number;
  npq: number;
  busIndex: Map<string, number>;
}

export interface NRState {
  V: Complex[];
  Psp: number[];
  Qsp: number[];
  converged: boolean;
  iterations: number;
  maxMismatch: number;
}

export function buildYBus(system: PowerSystem): { Y: YBusMatrix; busIndex: Map<string, number> } {
  const n = system.buses.length;
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  const Y: YBusMatrix = {};
  for (let i = 0; i < n; i++) { Y[i] = {}; for (let j = 0; j < n; j++) Y[i][j] = { g: 0, b: 0 }; }

  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus)!, j = busIndex.get(line.toBus)!;
    const denom = line.resistance * line.resistance + line.reactance * line.reactance;
    if (denom === 0) return;
    const g = line.resistance / denom, b = -line.reactance / denom;
    Y[i][j].g -= g; Y[i][j].b -= b;
    Y[j][i].g -= g; Y[j][i].b -= b;
    Y[i][i].g += g; Y[i][i].b += b + line.susceptance / 2;
    Y[j][j].g += g; Y[j][j].b += b + line.susceptance / 2;
  });

  system.transformers.forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus)!, j = busIndex.get(txf.toBus)!;
    const tap = txf.tap > 0 ? txf.tap : 1, z = txf.impedance;
    if (z === 0) return;
    const g = 1 / z;
    Y[i][j].g -= g / tap; Y[i][j].b += txf.phase ? -txf.phase / z : 0;
    Y[j][i].g -= g / tap; Y[j][i].b += txf.phase ? txf.phase / z : 0;
    Y[i][i].g += g / (tap * tap);
    Y[j][j].g += g;
  });

  system.shunts.forEach(shunt => {
    if (!shunt.active) return;
    const i = busIndex.get(shunt.busId)!;
    Y[i][i].g += shunt.g; Y[i][i].b += shunt.b;
  });

  return { Y, busIndex };
}

export function getIndices(system: PowerSystem): SystemIndices {
  const n = system.buses.length;
  const slackIdx = system.buses.findIndex(b => b.type === 'slack');
  const pvIndices = system.buses.map((b, i) => b.type === 'pv' ? i : -1).filter(i => i >= 0);
  const pqIndices = system.buses.map((b, i) => b.type === 'pq' ? i : -1).filter(i => i >= 0);
  const thetaMap: number[] = [];
  for (let i = 0; i < n; i++) if (i !== slackIdx) thetaMap.push(i);
  const busIndex = new Map<string, number>();
  system.buses.forEach((b, i) => busIndex.set(b.id, i));
  return { n, slackIdx, pvIndices, pqIndices, thetaMap, ntheta: n - 1, npq: pqIndices.length, busIndex };
}

export function calcPQI(i: number, V: Complex[], Y: YBusMatrix): { p: number; q: number } {
  let p = 0, q = 0;
  const n = V.length;
  for (let j = 0; j < n; j++) {
    const yij = Y[i]?.[j] || { g: 0, b: 0 };
    const theta = cAngle(V[i]) - cAngle(V[j]);
    const vv = cAbs(V[i]) * cAbs(V[j]);
    p += vv * (yij.g * Math.cos(theta) + yij.b * Math.sin(theta));
    q += vv * (yij.g * Math.sin(theta) - yij.b * Math.cos(theta));
  }
  return { p, q };
}

export function calcAllPQI(V: Complex[], Y: YBusMatrix): { Pcalc: number[]; Qcalc: number[] } {
  const n = V.length;
  const Pcalc = new Array(n).fill(0);
  const Qcalc = new Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    const { p, q } = calcPQI(i, V, Y);
    Pcalc[i] = p; Qcalc[i] = q;
  }
  return { Pcalc, Qcalc };
}

export function getScheduledPower(system: PowerSystem, busIndex: Map<string, number>): { Psp: number[]; Qsp: number[] } {
  const n = system.buses.length;
  const Psp = new Array(n).fill(0);
  const Qsp = new Array(n).fill(0);
  system.generators.forEach(gen => {
    if (!gen.active) return;
    const idx = busIndex.get(gen.busId);
    if (idx !== undefined) { Psp[idx] += gen.pGen; Qsp[idx] -= gen.qGen; }
  });
  system.loads.forEach(load => {
    if (!load.active) return;
    const idx = busIndex.get(load.busId);
    if (idx !== undefined) { Psp[idx] -= load.pDemand; Qsp[idx] += load.qDemand; }
  });
  return { Psp, Qsp };
}

export function buildFullJacobian(V: Complex[], Y: YBusMatrix, indices: SystemIndices): number[][] {
  const { n, slackIdx, pqIndices, thetaMap, ntheta, npq } = indices;
  const sz = ntheta + npq;
  const J = Array.from({ length: sz }, () => new Array(sz).fill(0));
  const { Pcalc, Qcalc } = calcAllPQI(V, Y);

  for (let ii = 0; ii < ntheta; ii++) {
    const i = thetaMap[ii];
    const Vi = cAbs(V[i]), tI = cAngle(V[i]);

    for (let jj = 0; jj < ntheta; jj++) {
      const j = thetaMap[jj];
      if (i === j) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
          if (k === i) continue;
          const y = Y[i]?.[k] || { g: 0, b: 0 };
          sum += cAbs(V[k]) * (y.g * Math.sin(tI - cAngle(V[k])) - y.b * Math.cos(tI - cAngle(V[k])));
        }
        J[ii][jj] = -Qcalc[i] - sum * Vi;
      } else {
        const y = Y[i]?.[j] || { g: 0, b: 0 };
        J[ii][jj] = Vi * cAbs(V[j]) * (y.g * Math.sin(tI - cAngle(V[j])) - y.b * Math.cos(tI - cAngle(V[j])));
      }
    }

    for (let qi = 0; qi < npq; qi++) {
      const j = pqIndices[qi];
      const y = Y[i]?.[j] || { g: 0, b: 0 };
      J[ii][ntheta + qi] = Vi * (y.g * Math.cos(tI - cAngle(V[j])) + y.b * Math.sin(tI - cAngle(V[j])));
    }
  }

  for (let qi = 0; qi < npq; qi++) {
    const i = pqIndices[qi];
    const Vi = cAbs(V[i]), tI = cAngle(V[i]);

    for (let jj = 0; jj < ntheta; jj++) {
      const j = thetaMap[jj];
      if (i === j) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
          if (k === i) continue;
          const y = Y[i]?.[k] || { g: 0, b: 0 };
          sum += cAbs(V[k]) * (y.g * Math.cos(tI - cAngle(V[k])) + y.b * Math.sin(tI - cAngle(V[k])));
        }
        J[ntheta + qi][jj] = Pcalc[i] - sum * Vi;
      } else {
        const y = Y[i]?.[j] || { g: 0, b: 0 };
        J[ntheta + qi][jj] = -Vi * cAbs(V[j]) * (y.g * Math.cos(tI - cAngle(V[j])) + y.b * Math.sin(tI - cAngle(V[j])));
      }
    }

    for (let qj = 0; qj < npq; qj++) {
      const j = pqIndices[qj];
      if (i === j) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
          if (k === i) continue;
          const y = Y[i]?.[k] || { g: 0, b: 0 };
          sum += cAbs(V[k]) * (y.g * Math.sin(tI - cAngle(V[k])) - y.b * Math.cos(tI - cAngle(V[k])));
        }
        J[ntheta + qi][ntheta + qj] = Qcalc[i] / Vi - sum;
      } else {
        const y = Y[i]?.[j] || { g: 0, b: 0 };
        J[ntheta + qi][ntheta + qj] = Vi * (y.g * Math.sin(tI - cAngle(V[j])) - y.b * Math.cos(tI - cAngle(V[j])));
      }
    }
  }

  return J;
}

export function buildMismatchVector(V: Complex[], Psp: number[], Qsp: number[], Y: YBusMatrix, indices: SystemIndices): { mis: number[]; maxMismatch: number } {
  const { n, slackIdx, pqIndices, thetaMap, ntheta, npq } = indices;
  const { Pcalc, Qcalc } = calcAllPQI(V, Y);
  const sz = ntheta + npq;
  const mis = new Array(sz).fill(0);
  let maxMismatch = 0;

  for (let ii = 0; ii < ntheta; ii++) {
    const i = thetaMap[ii];
    mis[ii] = Psp[i] - Pcalc[i];
    maxMismatch = Math.max(maxMismatch, Math.abs(mis[ii]));
  }
  for (let qi = 0; qi < npq; qi++) {
    const i = pqIndices[qi];
    mis[ntheta + qi] = Qsp[i] + Qcalc[i];
    maxMismatch = Math.max(maxMismatch, Math.abs(mis[ntheta + qi]));
  }

  return { mis, maxMismatch };
}

export function doNRStep(state: NRState, Y: YBusMatrix, indices: SystemIndices, pvVoltages?: number[]): boolean {
  const { n, slackIdx, pvIndices, pqIndices, thetaMap, ntheta, npq } = indices;
  const { V, Psp, Qsp } = state;

  const J = buildFullJacobian(V, Y, indices);
  const { mis, maxMismatch } = buildMismatchVector(V, Psp, Qsp, Y, indices);
  state.maxMismatch = maxMismatch;

  if (maxMismatch < 1e-8) { state.converged = true; return true; }

  try {
    const inc = solveLU(J, mis);
    for (let ii = 0; ii < ntheta; ii++) {
      const i = thetaMap[ii];
      V[i] = cPolar(cAbs(V[i]), cAngle(V[i]) + inc[ii]);
    }
    for (let qi = 0; qi < npq; qi++) {
      const i = pqIndices[qi];
      V[i] = cPolar(cAbs(V[i]) * (1 + inc[ntheta + qi]), cAngle(V[i]));
    }
    if (pvVoltages) {
      pvIndices.forEach(pi => { V[pi] = cPolar(pvVoltages[pi], cAngle(V[pi])); });
    } else {
      pvIndices.forEach(pi => { V[pi] = cPolar(cAbs(V[pi]), cAngle(V[pi])); });
    }
    if (slackIdx >= 0) { V[slackIdx] = cPolar(cAbs(V[slackIdx]), 0); }
  } catch { return false; }

  return false;
}

export function solveNR(V: Complex[], Psp: number[], Qsp: number[], Y: YBusMatrix, indices: SystemIndices, maxIter: number = 50, tol: number = 1e-8): { converged: boolean; iterations: number; maxMismatch: number } {
  const state: NRState = { V, Psp, Qsp, converged: false, iterations: 0, maxMismatch: 0 };
  const pvVoltages = indices.pvIndices.map(pi => V[pi] ? cAbs(V[pi]) : 1.0);

  for (let iter = 0; iter < maxIter; iter++) {
    state.iterations = iter;
    if (doNRStep(state, Y, indices, pvVoltages)) break;
  }

  indices.pvIndices.forEach((pi, i) => { V[pi] = cPolar(pvVoltages[i], cAngle(V[pi])); });
  return { converged: state.converged, iterations: state.iterations, maxMismatch: state.maxMismatch };
}

export function initializeV(system: PowerSystem, flatStart: boolean = true): Complex[] {
  const V: Complex[] = new Array(system.buses.length);
  system.buses.forEach((bus, i) => {
    V[i] = flatStart
      ? (bus.type === 'slack' ? cPolar(bus.voltage, 0) : cPolar(1.0, 0))
      : cPolar(bus.voltage, bus.angle * Math.PI / 180);
  });
  return V;
}

export function calcBusResults(system: PowerSystem, V: Complex[], busIndex: Map<string, number>): import('@/types').BusResult[] {
  return system.buses.map(bus => {
    const idx = busIndex.get(bus.id)!;
    let pGen = 0, qGen = 0, pLoad = 0, qLoad = 0;
    system.generators.forEach(g => { if (g.busId === bus.id && g.active) { pGen += g.pGen; qGen += g.qGen; } });
    system.loads.forEach(l => { if (l.busId === bus.id && l.active) { pLoad += l.pDemand; qLoad += l.qDemand; } });
    return { id: bus.id, voltage: cAbs(V[idx]), angle: cDeg(V[idx]), pGen, qGen, pLoad, qLoad };
  });
}

export function calcLineResults(system: PowerSystem, V: Complex[], busIndex: Map<string, number>): import('@/types').LineResult[] {
  const Y = buildYBus(system).Y;
  return system.lines.map(line => {
    const fi = busIndex.get(line.fromBus)!, ti = busIndex.get(line.toBus)!;
    const denom = line.resistance * line.resistance + line.reactance * line.reactance;
    if (denom === 0) return { id: line.id, pFrom: 0, qFrom: 0, pTo: 0, qTo: 0, loading: 0 };
    const g = line.resistance / denom, b = -line.reactance / denom;
    const IijF = { real: g * V[fi].real - b * V[fi].imag - (g * V[ti].real - b * V[ti].imag), imag: g * V[fi].imag + b * V[fi].real - (g * V[ti].imag + b * V[ti].real) };
    const IijT = { real: g * V[ti].real - b * V[ti].imag - (g * V[fi].real - b * V[fi].imag), imag: g * V[ti].imag + b * V[ti].real - (g * V[fi].imag + b * V[fi].real) };
    const Sij = { real: V[fi].real * IijF.real + V[fi].imag * IijF.imag, imag: V[fi].real * IijF.imag - V[fi].imag * IijF.real };
    const Sji = { real: V[ti].real * IijT.real + V[ti].imag * IijT.imag, imag: V[ti].real * IijT.imag - V[ti].imag * IijT.real };
    const IijMag = Math.sqrt(IijF.real * IijF.real + IijF.imag * IijF.imag);
    const loading = line.rating > 0 ? IijMag * cAbs(V[fi]) / line.rating * 100 : IijMag * 100;
    return { id: line.id, pFrom: Sij.real, qFrom: -Sij.imag, pTo: Sji.real, qTo: -Sji.imag, loading };
  });
}

export function calcLosses(system: PowerSystem, V: Complex[], busIndex: Map<string, number>): { real: number; reactive: number } {
  let pLoss = 0, qLoss = 0;
  system.lines.forEach(line => {
    const fi = busIndex.get(line.fromBus)!, ti = busIndex.get(line.toBus)!;
    const denom = line.resistance * line.resistance + line.reactance * line.reactance;
    if (denom === 0) return;
    const g = line.resistance / denom, b = -line.reactance / denom;
    const Iij = { real: g * V[fi].real - b * V[fi].imag - (g * V[ti].real - b * V[ti].imag), imag: g * V[fi].imag + b * V[fi].real - (g * V[ti].imag + b * V[ti].real) };
    pLoss += line.resistance * (Iij.real * Iij.real + Iij.imag * Iij.imag);
    qLoss += line.reactance * (Iij.real * Iij.real + Iij.imag * Iij.imag);
  });
  return { real: pLoss, reactive: qLoss };
}
