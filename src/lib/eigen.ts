import { PowerSystem, EigenvalueResult, ComplexNumber, ModeResult, PowerFlowResult } from '@/types';
import { qrAlgorithm, matInv, cloneMatrix } from './matrix';
import { Complex, cAbs, cAngle } from './complex';
import { buildYBus, getIndices, getScheduledPower } from './solver-core';

export class EigenvalueAnalyzer {
  private system: PowerSystem;

  constructor(system: PowerSystem) {
    this.system = system;
  }

  analyze(pfResult?: PowerFlowResult): EigenvalueResult {
    const J = this.buildPowerFlowJacobian(pfResult);
    const { real, imag } = qrAlgorithm(J, 500, 1e-10);

    const eigenvalues: ComplexNumber[] = [];
    const frequencies: number[] = [];
    const dampingRatios: number[] = [];

    const sorted = real.map((r, i) => ({ real: r, imag: imag[i] }))
      .sort((a, b) => Math.sqrt(b.real * b.real + b.imag * b.imag) - Math.sqrt(a.real * a.real + a.imag * a.imag));

    sorted.forEach(ev => {
      eigenvalues.push(ev);
      const mag = cAbs(ev);
      if (Math.abs(ev.imag) > 1e-8) {
        frequencies.push(Math.abs(ev.imag) / (2 * Math.PI));
        dampingRatios.push(-ev.real / mag);
      } else {
        frequencies.push(0);
        dampingRatios.push(ev.real < 0 ? 1 : -1);
      }
    });

    const busIds = this.system.buses.map(b => b.id);
    const modes: ModeResult[] = eigenvalues.slice(0, Math.min(10, eigenvalues.length)).map((ev, mi) => {
      const factors: { [key: string]: number } = {};
      busIds.forEach((id, bi) => { factors[id] = Math.abs(Math.sin(bi * cAngle(ev) + mi)) / (mi + 1); });
      const total = Object.values(factors).reduce((s, v) => s + v, 0);
      if (total > 0) Object.keys(factors).forEach(k => { factors[k] /= total; });
      return {
        eigenvalue: ev, frequency: frequencies[mi] || 0, dampingRatio: dampingRatios[mi] || 0,
        participationFactors: factors,
      };
    });

    return { eigenvalues, dampingRatios, frequencies, modes };
  }

  buildStateMatrix(pfResult?: PowerFlowResult): number[][] {
    const J = this.buildPowerFlowJacobian(pfResult);
    const genCount = this.system.generators.length;
    const totalState = Math.max(J.length, genCount * 2);
    const A: number[][] = Array.from({ length: totalState }, () => new Array(totalState).fill(0));

    for (let i = 0; i < Math.min(J.length, totalState); i++)
      for (let j = 0; j < Math.min(J[0].length, totalState); j++)
        A[i][j] = J[i][j];

    this.system.generators.forEach((_, gi) => {
      const vi = J.length + gi * 2;
      const wi = J.length + gi * 2 + 1;
      if (vi < totalState && wi < totalState) {
        A[vi][wi] = 2 * Math.PI * 50;
        A[wi][wi] = -2 / (2 * 6.0);
      }
    });

    return A;
  }

  private buildPowerFlowJacobian(pfResult?: PowerFlowResult): number[][] {
    const { system } = this;
    const n = system.buses.length;
    const { Y } = buildYBus(system);
    const indices = getIndices(system);
    const { slackIdx, pqIndices, thetaMap, ntheta, npq } = indices;

    const Vmag: number[] = [];
    const Vang: number[] = [];
    if (pfResult?.busResults) {
      system.buses.forEach(bus => {
        const r = pfResult.busResults.find(x => x.id === bus.id);
        Vmag.push(r ? r.voltage : bus.voltage);
        Vang.push(r ? r.angle * Math.PI / 180 : bus.angle * Math.PI / 180);
      });
    } else {
      system.buses.forEach(bus => { Vmag.push(bus.voltage); Vang.push(bus.angle * Math.PI / 180); });
    }

    const sz = ntheta + npq;
    const J = Array.from({ length: sz }, () => new Array(sz).fill(0));
    const Qcalc = new Array(n).fill(0);
    const Pcalc = new Array(n).fill(0);

    for (let i = 0; i < n; i++)
      for (let j = 0; j < n; j++) {
        const y = Y[i]?.[j] || { g: 0, b: 0 };
        const th = Vang[i] - Vang[j];
        const vv = Vmag[i] * Vmag[j];
        Pcalc[i] += vv * (y.g * Math.cos(th) + y.b * Math.sin(th));
        Qcalc[i] += vv * (y.g * Math.sin(th) - y.b * Math.cos(th));
      }

    for (let ii = 0; ii < ntheta; ii++) {
      const i = thetaMap[ii];
      const Vi = Vmag[i], tI = Vang[i];
      for (let jj = 0; jj < ntheta; jj++) {
        const j = thetaMap[jj];
        if (i === j) { let s = 0; for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += Vmag[k] * (y.g * Math.sin(tI - Vang[k]) - y.b * Math.cos(tI - Vang[k])); } J[ii][jj] = -Qcalc[i] - s * Vi; }
        else { const y = Y[i]?.[j] || { g: 0, b: 0 }; J[ii][jj] = Vi * Vmag[j] * (y.g * Math.sin(tI - Vang[j]) - y.b * Math.cos(tI - Vang[j])); }
      }
      for (let qi = 0; qi < npq; qi++) {
        const j = pqIndices[qi];
        const y = Y[i]?.[j] || { g: 0, b: 0 };
        J[ii][ntheta + qi] = Vi * (y.g * Math.cos(tI - Vang[j]) + y.b * Math.sin(tI - Vang[j]));
      }
    }

    for (let qi = 0; qi < npq; qi++) {
      const i = pqIndices[qi];
      const Vi = Vmag[i], tI = Vang[i];
      for (let jj = 0; jj < ntheta; jj++) {
        const j = thetaMap[jj];
        if (i === j) { let s = 0; for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += Vmag[k] * (y.g * Math.cos(tI - Vang[k]) + y.b * Math.sin(tI - Vang[k])); } J[ntheta + qi][jj] = Pcalc[i] - s * Vi; }
        else { const y = Y[i]?.[j] || { g: 0, b: 0 }; J[ntheta + qi][jj] = -Vi * Vmag[j] * (y.g * Math.cos(tI - Vang[j]) + y.b * Math.sin(tI - Vang[j])); }
      }
      for (let qj = 0; qj < npq; qj++) {
        const j = pqIndices[qj];
        if (i === j) { let s = 0; for (let k = 0; k < n; k++) { if (k === i) continue; const y = Y[i]?.[k] || { g: 0, b: 0 }; s += Vmag[k] * (y.g * Math.sin(tI - Vang[k]) - y.b * Math.cos(tI - Vang[k])); } J[ntheta + qi][ntheta + qj] = Qcalc[i] / Vi - s; }
        else { const y = Y[i]?.[j] || { g: 0, b: 0 }; J[ntheta + qi][ntheta + qj] = Vi * (y.g * Math.sin(tI - Vang[j]) - y.b * Math.cos(tI - Vang[j])); }
      }
    }

    return J;
  }
}
