/**
 * Power Flow Analysis Module
 * Delegates to powerflow-methods for all computation.
 * Maintains PowerFlowSolver class for backward compatibility.
 */

import { PowerSystem, PowerFlowResult, BusResult, LineResult, GeneratorResult } from '@/types';
import { solveNewtonRaphson, buildYBus } from './powerflow-methods';

/**
 * PowerFlowSolver - maintained for backward compatibility with existing tests
 */
export class PowerFlowSolver {
  private system: PowerSystem;
  private lastResult: PowerFlowResult | null = null;
  
  constructor(system: PowerSystem) {
    this.system = system;
  }
  
  public buildYBus(): void {
    // Verify YBus can be built without error
    const ybus = buildYBus(this.system);
    if (ybus.n !== this.system.buses.length) {
      throw new Error('YBus dimension mismatch');
    }
  }
  
  public solve(): PowerFlowResult {
    // Use the full Newton-Raphson implementation from powerflow-methods
    this.lastResult = solveNewtonRaphson(this.system, 1e-8, 50);
    return this.lastResult;
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
      { id: 'LD3', bus: '3', pl: 1.0, ql: 0.5, active: true },
      { id: 'LD4', bus: '4', pl: 0.7, ql: 0.35, active: true },
    ],
    generators: [
      { id: 'G1', bus: '1', pg: 0.8, qg: 0, v: 1.0, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
      { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.05, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
    baseMVA: 100,
    baseFreq: 60
  };
}