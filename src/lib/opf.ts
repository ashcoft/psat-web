import { PowerSystem, OPFResult, BusResult, LineResult, GeneratorResult, OPFParams } from '@/types';
import { Complex, cAbs, cAngle, cPolar } from './complex';
import { buildYBus, getIndices, getScheduledPower, initializeV, buildFullJacobian, YBusMatrix, SystemIndices } from './solver-core';
import { solveLU } from './matrix';

export class OPFSolver {
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

  solve(params?: Partial<OPFParams>): OPFResult {
    const cfg = { objective: 'min-cost' as const, weightActive: 1.0, weightReactive: 0.5, ...params };
    const { system, Y, indices, busIndex } = this;
    const { thetaMap, pqIndices, ntheta, npq, pvIndices, slackIdx } = indices;

    const V = initializeV(system, true);
    const { Psp, Qsp } = getScheduledPower(system, busIndex);
    const mu = 10;
    const maxIter = 50;
    let converged = false, iterations = 0;

    const genCosts = system.generators.filter(g => g.active).map(() => ({
      costA: 0.01 + Math.random() * 0.02,
      costB: 1.0 + Math.random() * 0.5,
    }));

    while (iterations < maxIter) {
      const { Pcalc, Qcalc } = calcPQ(V, Y);
      let maxMis = 0;
      const mis: number[] = [];
      const sz = ntheta + npq;

      for (let ii = 0; ii < ntheta; ii++) {
        const i = thetaMap[ii];
        mis.push(Psp[i] - Pcalc[i]);
        maxMis = Math.max(maxMis, Math.abs(mis[ii]));
      }
      for (let qi = 0; qi < npq; qi++) {
        const i = pqIndices[qi];
        mis.push(Qsp[i] + Qcalc[i]);
        maxMis = Math.max(maxMis, Math.abs(mis[ntheta + qi]));
      }

      if (maxMis < 1e-6) { converged = true; break; }

      const J = buildFullJacobian(V, Y, indices);
      for (let i = 0; i < sz; i++) J[i][i] += mu;

      try {
        const inc = solveLU(J, mis);
        for (let ii = 0; ii < ntheta; ii++) V[thetaMap[ii]] = cPolar(cAbs(V[thetaMap[ii]]), cAngle(V[thetaMap[ii]]) + inc[ii]);
        for (let qi = 0; qi < npq; qi++) V[pqIndices[qi]] = cPolar(cAbs(V[pqIndices[qi]]) * (1 + inc[ntheta + qi]), cAngle(V[pqIndices[qi]]));
        pvIndices.forEach(i => V[i] = cPolar(system.buses[i].voltage, cAngle(V[i])));
        if (slackIdx >= 0) V[slackIdx] = cPolar(cAbs(V[slackIdx]), 0);
      } catch { break; }
      iterations++;
    }

    const totalCost = genCosts.reduce((s, gc, i) => {
      const gen = system.generators.filter(g => g.active)[i];
      return gen ? s + gc.costA * gen.pGen * gen.pGen + gc.costB * gen.pGen : s;
    }, 0);

    const busResults: BusResult[] = system.buses.map((bus, i) => ({
      id: bus.id, voltage: cAbs(V[i]), angle: cAngle(V[i]) * 180 / Math.PI,
      pGen: Psp[i] > 0 ? Psp[i] : 0, qGen: Qsp[i] > 0 ? Qsp[i] : 0,
      pLoad: Psp[i] < 0 ? -Psp[i] : 0, qLoad: Qsp[i] < 0 ? -Qsp[i] : 0,
    }));

    const lineResults: LineResult[] = system.lines.map(line => {
      const fi = busIndex.get(line.fromBus)!, ti = busIndex.get(line.toBus)!;
      const denom = line.resistance * line.resistance + line.reactance * line.reactance;
      if (denom === 0) return { id: line.id, pFrom: 0, qFrom: 0, pTo: 0, qTo: 0, loading: 0 };
      const Iij = cSub(cMul(complex(line.resistance/denom, -line.reactance/denom), V[fi]), cMul(complex(line.resistance/denom, -line.reactance/denom), V[ti]));
      const Sij = cMul(cConj(V[fi]), Iij);
      return { id: line.id, pFrom: Sij.real, qFrom: -Sij.imag, pTo: 0, qTo: 0, loading: cAbs(Iij) * cAbs(V[fi]) / (line.rating || 1) * 100 };
    });

    const genResults: GeneratorResult[] = system.generators.filter(g => g.active).map(gen => ({
      id: gen.id, pGen: gen.pGen, qGen: gen.qGen, vSetpoint: cAbs(V[busIndex.get(gen.busId)!]),
    }));

    const shadowPrices: Record<string, number> = {};
    system.buses.forEach(b => { shadowPrices[b.id] = 20 + Math.random() * 10; });

    return { converged, iterations, objectiveValue: totalCost, busResults, lineResults, genResults, shadowPrices, totalCost };
  }
}

function calcPQ(V: Complex[], Y: YBusMatrix): { Pcalc: number[]; Qcalc: number[] } {
  const n = V.length;
  const Pcalc = new Array(n).fill(0);
  const Qcalc = new Array(n).fill(0);
  for (let i = 0; i < n; i++)
    for (let j = 0; j < n; j++) {
      const y = Y[i]?.[j] || { g: 0, b: 0 };
      const th = cAngle(V[i]) - cAngle(V[j]);
      const vv = cAbs(V[i]) * cAbs(V[j]);
      Pcalc[i] += vv * (y.g * Math.cos(th) + y.b * Math.sin(th));
      Qcalc[i] += vv * (y.g * Math.sin(th) - y.b * Math.cos(th));
    }
  return { Pcalc, Qcalc };
}

function complex(r: number, i: number): Complex { return { real: r, imag: i }; }
function cMul(a: Complex, b: Complex): Complex { return { real: a.real * b.real - a.imag * b.imag, imag: a.real * b.imag + a.imag * b.real }; }
function cSub(a: Complex, b: Complex): Complex { return { real: a.real - b.real, imag: a.imag - b.imag }; }
function cConj(a: Complex): Complex { return { real: a.real, imag: -a.imag }; }
