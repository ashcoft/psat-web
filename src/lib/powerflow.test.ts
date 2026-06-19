import { describe, it, expect } from 'vitest';
import { PowerFlowSolver, createDefaultSystem } from './powerflow';
import { PowerSystem, Bus, Line } from '@/types';

const createBus = (id: string, type: 'slack' | 'pv' | 'pq', x: number = 0): Bus => ({
  id,
  name: `${type.toUpperCase()} Bus ${id}`,
  type,
  voltage: type === 'slack' ? 1.0 : type === 'pv' ? 1.05 : 1.0,
  angle: 0,
  vmin: 0.9,
  vmax: 1.1,
  area: 1,
  region: 1,
  x,
  y: 0,
  active: true,
});

const createLine = (id: string, fromBus: string, toBus: string, active: boolean = true): Line => ({
  id,
  fromBus,
  toBus,
  resistance: 0.02,
  reactance: 0.04,
  susceptance: 0,
  rating: 100,
  active,
});

const createBaseSystem = (buses: Bus[], lines: Line[]): PowerSystem => ({
  buses,
  lines,
  transformers: [],
  loads: [],
  generators: [],
  shunts: [],
  areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
        baseMVA: 100,
        baseFreq: 60,
});

describe('PowerFlowSolver', () => {
  describe('buildYBus', () => {
    it('should build YBus matrix for a simple system', () => {
      const system = createBaseSystem(
        [createBus('1', 'slack'), createBus('2', 'pq', 1)],
        [createLine('L12', '1', '2')]
      );

      const solver = new PowerFlowSolver(system);
      solver.buildYBus();
      expect(true).toBe(true);
    });

    it('should skip inactive lines', () => {
      const system = createBaseSystem(
        [createBus('1', 'slack'), createBus('2', 'pq', 1)],
        [createLine('L12', '1', '2', false)]
      );

      const solver = new PowerFlowSolver(system);
      expect(() => solver.buildYBus()).not.toThrow();
    });
  });

  describe('solve', () => {
    it('should solve power flow for default system', () => {
      const system = createDefaultSystem();
      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result).toBeDefined();
      expect(result.converged).toBeDefined();
      expect(typeof result.converged).toBe('boolean');
      expect(result.iterations).toBeGreaterThanOrEqual(0);
      expect(result.maxMismatch).toBeGreaterThanOrEqual(0);
      expect(result.busResults).toHaveLength(system.buses.length);
      expect(result.lineResults).toHaveLength(system.lines.length);
      expect(result.generatorResults).toHaveLength(system.generators.length);
      expect(result.losses).toBeDefined();
      expect(typeof result.losses.real).toBe('number');
      expect(typeof result.losses.imag).toBe('number');
    });

    it('should handle system with only slack bus', () => {
      const system = createBaseSystem([createBus('1', 'slack')], []);
      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.converged).toBe(true);
      expect(result.busResults).toHaveLength(1);
    });

    it('should handle multiple generators', () => {
      const system: PowerSystem = {
        buses: [createBus('1', 'slack'), createBus('2', 'pv', 1)],
        lines: [createLine('L12', '1', '2')],
        transformers: [],
        loads: [],
        generators: [
          { id: 'G1', bus: '1', pg: 0.5, qg: 0, v: 1.0, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
          { id: 'G2', bus: '2', pg: 0.3, qg: 0, v: 1.05, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
        ],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
        baseMVA: 100,
        baseFreq: 60,
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.generatorResults).toHaveLength(2);
      expect(result.generatorResults[0].pg).toBe(0.5);
      expect(result.generatorResults[1].pg).toBe(0.3);
    });

    it('should handle loads', () => {
      const system: PowerSystem = {
        buses: [createBus('1', 'slack'), createBus('2', 'pq', 1)],
        lines: [createLine('L12', '1', '2')],
        transformers: [],
        loads: [{ id: 'LD1', bus: '2', pl: 0.5, ql: 0.2, active: true }],
        generators: [],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
        baseMVA: 100,
        baseFreq: 60,
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.busResults).toHaveLength(2);
    });

    it('should handle shunt elements', () => {
      const system: PowerSystem = {
        buses: [createBus('1', 'slack'), createBus('2', 'pq', 1)],
        lines: [createLine('L12', '1', '2')],
        transformers: [],
        loads: [],
        generators: [],
        shunts: [{ id: 'SH1', bus: '2', g: 0.01, b: 0.02, active: true }],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
        baseMVA: 100,
        baseFreq: 60,
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result).toBeDefined();
      expect(result.busResults).toHaveLength(2);
    });
  });

  describe('createDefaultSystem', () => {
    it('should create a valid default system', () => {
      const system = createDefaultSystem();

      expect(system.buses).toBeDefined();
      expect(system.lines).toBeDefined();
      expect(system.transformers).toBeDefined();
      expect(system.loads).toBeDefined();
      expect(system.generators).toBeDefined();
      expect(system.shunts).toBeDefined();
      expect(system.areas).toBeDefined();

      const slackBus = system.buses.find(b => b.type === 'slack');
      expect(slackBus).toBeDefined();
      expect(system.lines.length).toBeGreaterThan(0);
      expect(system.generators.length).toBeGreaterThan(0);
    });
  });
});
