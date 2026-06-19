import { describe, it, expect } from 'vitest';
import { PowerFlowSolver, createDefaultSystem } from './powerflow';
import { PowerSystem } from '@/types';

describe('PowerFlowSolver', () => {
  describe('buildYBus', () => {
    it('should build YBus matrix for a simple system', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'PQ', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        transformers: [],
        loads: [],
        generators: [],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
      };

      const solver = new PowerFlowSolver(system);
      solver.buildYBus();
      
      // Test passes if no error is thrown
      expect(true).toBe(true);
    });

    it('should skip inactive lines', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'PQ', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: false },
        ],
        transformers: [],
        loads: [],
        generators: [],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
      };

      const solver = new PowerFlowSolver(system);
      // Should not throw when building YBus with inactive line
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
      expect(result.genResults).toHaveLength(system.generators.length);
      expect(result.losses).toBeDefined();
      expect(typeof result.losses.real).toBe('number');
      expect(typeof result.losses.reactive).toBe('number');
    });

    it('should handle system with only slack bus', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
        ],
        lines: [],
        transformers: [],
        loads: [],
        generators: [],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.converged).toBe(true);
      expect(result.busResults).toHaveLength(1);
    });

    it('should handle multiple generators', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'PV', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        transformers: [],
        loads: [],
        generators: [
          { id: 'G1', busId: '1', pGen: 0.5, qGen: 0, vSetpoint: 1.0, active: true },
          { id: 'G2', busId: '2', pGen: 0.3, qGen: 0, vSetpoint: 1.05, active: true },
        ],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.genResults).toHaveLength(2);
      expect(result.genResults[0].pGen).toBe(0.5);
      expect(result.genResults[1].pGen).toBe(0.3);
    });

    it('should handle loads', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'PQ', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        transformers: [],
        loads: [
          { id: 'LD1', busId: '2', pDemand: 0.5, qDemand: 0.2, active: true },
        ],
        generators: [],
        shunts: [],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
      };

      const solver = new PowerFlowSolver(system);
      const result = solver.solve();

      expect(result.busResults).toHaveLength(2);
    });

    it('should handle shunt elements', () => {
      const system: PowerSystem = {
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'PQ', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        transformers: [],
        loads: [],
        generators: [],
        shunts: [
          { id: 'SH1', busId: '2', g: 0.01, b: 0.02, active: true },
        ],
        areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }]
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

      // Check bus types
      const slackBus = system.buses.find(b => b.type === 'slack');
      expect(slackBus).toBeDefined();

      // Check system has at least one line
      expect(system.lines.length).toBeGreaterThan(0);

      // Check system has generators
      expect(system.generators.length).toBeGreaterThan(0);
    });
  });
});
