import { PowerSystem, SimulationParams, SimulationResult } from '@/types';
import { Complex, cAbs, cAngle, cPolar } from './complex';
import {
  buildYBus, getIndices, getScheduledPower, initializeV,
  YBusMatrix, SystemIndices
} from './solver-core';
import { solveLU } from './matrix';

class SwingEq {
  constructor(public H: number, public D: number, public Pm: number, public delta: number, public omega: number, public ws: number) {}
  deriv(): [number, number] {
    return [this.omega - this.ws, (this.ws / (2 * this.H)) * (this.Pm - this.Pe - (this.D / this.ws) * (this.omega - this.ws))];
  }
  Pe: number = 0;
}

export class TimeDomainSimulator {
  private system: PowerSystem;
  private Y: YBusMatrix;
  private indices: SystemIndices;
  private busIndex: Map<string, number>;

  constructor(system: PowerSystem) {
    this.system = JSON.parse(JSON.stringify(system));
    const yRes = buildYBus(system);
    this.Y = yRes.Y;
    this.indices = getIndices(system);
    this.busIndex = yRes.busIndex;
  }

  simulate(params: SimulationParams, pfVmag?: number[], pfVang?: number[]): SimulationResult {
    const defaults = { tStart: 0, tEnd: 20, stepSize: 0.01, faultLocation: '', faultTime: 1.0, faultDuration: 0.1 };
    const cfg = { ...defaults, ...params };
    const { system, Y, indices, busIndex } = this;
    const { n, slackIdx, pvIndices, pqIndices, thetaMap, ntheta, npq } = indices;

    const V: Complex[] = new Array(n);
    system.buses.forEach((bus, i) => {
      V[i] = (pfVmag && pfVang) ? cPolar(pfVmag[i], pfVang[i] * Math.PI / 180) : initializeV(system, true)[i];
    });

    const ws = 2 * Math.PI * 50;
    const gens = system.generators.filter(g => g.active);
    const swings = gens.map((gen, i) => {
      const bi = busIndex.get(gen.busId)!;
      return new SwingEq(6.0, 2.0, gen.pGen, cAngle(V[bi]), ws, ws);
    });

    const time: number[] = [];
    const busV: Record<string, number[]> = {};
    const busA: Record<string, number[]> = {};
    const machD: Record<string, number[]> = {};
    const machW: Record<string, number[]> = {};
    system.buses.forEach(b => { busV[b.id] = []; busA[b.id] = []; });
    gens.forEach(g => { machD[g.id] = []; machW[g.id] = []; });

    const faultIdx = cfg.faultLocation ? busIndex.get(cfg.faultLocation) : undefined;
    const nSteps = Math.floor((cfg.tEnd - cfg.tStart) / cfg.stepSize);

    for (let step = 0; step <= nSteps; step++) {
      const t = cfg.tStart + step * cfg.stepSize;
      const dt = cfg.stepSize;
      const faultOn = t >= cfg.faultTime && t < cfg.faultTime + cfg.faultDuration;

      if (faultOn && faultIdx !== undefined) V[faultIdx] = cPolar(0, 0);

      const { Pcalc } = calcPQIall(V, Y);
      swings.forEach((sw, i) => {
        const bi = busIndex.get(gens[i].busId)!;
        sw.Pe = Pcalc[bi];
        const [dd, dw] = sw.deriv();
        sw.delta += dd * dt;
        sw.omega += dw * dt;
        V[bi] = cPolar(cAbs(V[bi]), sw.delta);
      });

      solveNetwork(V, Y, indices);

      time.push(t);
      system.buses.forEach((bus, i) => { busV[bus.id].push(cAbs(V[i])); busA[bus.id].push(cAngle(V[i]) * 180 / Math.PI); });
      gens.forEach((gen, i) => { machD[gen.id].push(swings[i].delta * 180 / Math.PI); machW[gen.id].push((swings[i].omega - ws) / ws * 100); });
    }

    return { time, busVoltages: busV, busAngles: busA, machineAngles: machD, machineSpeeds: machW };
  }
}

function calcPQIall(V: Complex[], Y: YBusMatrix): { Pcalc: number[]; Qcalc: number[] } {
  const n = V.length;
  const Pcalc = new Array(n).fill(0);
  const Qcalc = new Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const y = Y[i]?.[j] || { g: 0, b: 0 };
      const theta = cAngle(V[i]) - cAngle(V[j]);
      const vv = cAbs(V[i]) * cAbs(V[j]);
      Pcalc[i] += vv * (y.g * Math.cos(theta) + y.b * Math.sin(theta));
      Qcalc[i] += vv * (y.g * Math.sin(theta) - y.b * Math.cos(theta));
    }
  }
  return { Pcalc, Qcalc };
}

function solveNetwork(V: Complex[], Y: YBusMatrix, indices: SystemIndices): void {
  const { n, slackIdx, pqIndices, thetaMap, ntheta, npq } = indices;

  for (let iter = 0; iter < 20; iter++) {
    const { Pcalc, Qcalc } = calcPQIall(V, Y);
    let maxMis = 0;

    for (let ii = 0; ii < ntheta; ii++) {
      const i = thetaMap[ii];
      maxMis = Math.max(maxMis, Math.abs(Pcalc[i]));
    }
    pqIndices.forEach(i => { maxMis = Math.max(maxMis, Math.abs(Qcalc[i])); });

    if (maxMis < 1e-6) return;

    const sz = ntheta + npq;
    const J = Array.from({ length: sz }, () => new Array(sz).fill(0));
    const mis: number[] = [];

    for (let ii = 0; ii < ntheta; ii++) {
      const i = thetaMap[ii];
      const Vi = cAbs(V[i]), tI = cAngle(V[i]);
      for (let jj = 0; jj < ntheta; jj++) {
        const j = thetaMap[jj];
        if (i === j) {
          let s = 0;
          for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += cAbs(V[k]) * (y.g * Math.sin(tI - cAngle(V[k])) - y.b * Math.cos(tI - cAngle(V[k]))); }
          J[ii][jj] = -Qcalc[i] - s * Vi;
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
      mis.push(0);
    }

    for (let qi = 0; qi < npq; qi++) {
      const i = pqIndices[qi];
      const Vi = cAbs(V[i]), tI = cAngle(V[i]);
      for (let jj = 0; jj < ntheta; jj++) {
        const j = thetaMap[jj];
        if (i === j) {
          let s = 0;
          for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += cAbs(V[k]) * (y.g * Math.cos(tI - cAngle(V[k])) + y.b * Math.sin(tI - cAngle(V[k]))); }
          J[ntheta + qi][jj] = Pcalc[i] - s * Vi;
        } else {
          const y = Y[i]?.[j] || { g: 0, b: 0 };
          J[ntheta + qi][jj] = -Vi * cAbs(V[j]) * (y.g * Math.cos(tI - cAngle(V[j])) + y.b * Math.sin(tI - cAngle(V[j])));
        }
      }
      for (let qj = 0; qj < npq; qj++) {
        const j = pqIndices[qj];
        if (i === j) {
          let s = 0;
          for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += cAbs(V[k]) * (y.g * Math.sin(tI - cAngle(V[k])) - y.b * Math.cos(tI - cAngle(V[k]))); }
          J[ntheta + qi][ntheta + qj] = Qcalc[i] / Vi - s;
        } else {
          const y = Y[i]?.[j] || { g: 0, b: 0 };
          J[ntheta + qi][ntheta + qj] = Vi * (y.g * Math.sin(tI - cAngle(V[j])) - y.b * Math.cos(tI - cAngle(V[j])));
        }
      }
      mis.push(0);
    }

    try {
      const inc = solveLU(J, mis);
      for (let ii = 0; ii < ntheta; ii++) V[thetaMap[ii]] = cPolar(cAbs(V[thetaMap[ii]]), cAngle(V[thetaMap[ii]]) + inc[ii]);
      for (let qi = 0; qi < npq; qi++) V[pqIndices[qi]] = cPolar(cAbs(V[pqIndices[qi]]) * (1 + inc[ntheta + qi]), cAngle(V[pqIndices[qi]]));
      if (slackIdx >= 0) V[slackIdx] = cPolar(cAbs(V[slackIdx]), 0);
    } catch { return; }
  }
}
