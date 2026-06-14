import { PowerSystem, CPFResult, CPFPoint, CPFParams } from '@/types';
import { Complex, cAbs, cAngle, cPolar } from './complex';
import {
  buildYBus, getIndices, getScheduledPower, initializeV,
  buildFullJacobian, buildMismatchVector, solveNR,
  YBusMatrix, SystemIndices
} from './solver-core';
import { solveLU } from './matrix';

export class CPFSolver {
  private system: PowerSystem;
  private Y: YBusMatrix;
  private indices: SystemIndices;
  private busIndex: Map<string, number>;

  constructor(system: PowerSystem) {
    this.system = JSON.parse(JSON.stringify(system));
    this.busIndex = new Map();
    system.buses.forEach((bus, i) => this.busIndex.set(bus.id, i));
    const yRes = buildYBus(system);
    this.Y = yRes.Y;
    this.indices = getIndices(system);
  }

  solve(params?: Partial<CPFParams>): CPFResult {
    const config = { stepSize: 0.05, maxSteps: 200, targetLambda: 2.0, voltageLimit: 0.7, method: 'local' as const, showProgress: false, ...params };
    const { Y, indices, busIndex } = this;
    const { n, slackIdx, thetaMap, ntheta, npq, pqIndices, pvIndices } = indices;

    const V = initializeV(this.system, true);
    const { Psp: Psp0, Qsp: Qsp0 } = getScheduledPower(this.system, busIndex);
    const PspDir = Psp0.map(v => v * 0.3);
    const QspDir = Qsp0.map(v => v * 0.3);

    let lam = 0;
    let step = config.stepSize;
    const points: CPFPoint[] = [];
    let criticalLambda = 0, criticalBus = '';
    let converged = false;

    for (let s = 0; s < config.maxSteps; s++) {
      const Psp = Psp0.map((p, i) => p + lam * PspDir[i]);
      const Qsp = Qsp0.map((q, i) => q + lam * QspDir[i]);

      const nrResult = solveNR(V, Psp, Qsp, Y, indices, 50, 1e-6);
      if (!nrResult.converged) {
        step *= 0.5; lam -= step;
        if (step < 1e-6) break;
        continue;
      }

      pvIndices.forEach(i => { V[i] = cPolar(this.system.buses[i].voltage, cAngle(V[i])); });
      if (slackIdx >= 0) V[slackIdx] = cPolar(cAbs(V[slackIdx]), 0);

      const point: CPFPoint = { lambda: lam, busVoltages: {}, busAngles: {} };
      this.system.buses.forEach((bus, i) => {
        point.busVoltages[bus.id] = cAbs(V[i]);
        point.busAngles[bus.id] = cAngle(V[i]) * 180 / Math.PI;
      });
      points.push(point);

      const minV = Math.min(...this.system.buses.map(b => point.busVoltages[b.id]));
      if (minV < config.voltageLimit) {
        criticalLambda = lam;
        criticalBus = this.system.buses.reduce((a, b) => point.busVoltages[b.id] < point.busVoltages[a.id] ? b : a).id;
        converged = true;
        break;
      }

      lam += step;
    }

    const noseCurve = points.map(p => ({
      lambda: p.lambda,
      voltage: p.busVoltages[criticalBus || this.system.buses[0].id],
    }));

    return { points, criticalLambda, criticalBus, converged, noseCurve };
  }
}
