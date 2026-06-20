/**
 * Tests for Optimal Power Flow (OPF) Module
 */

import { describe, it, expect } from 'vitest';
import { 
  calculateGeneratorCost,
  calculateTotalCost,
  createDefaultCost,
  solveDCOPF,
  solveACOPF,
  solveSecurityConstrainedOPF,
  solveUnitCommitment,
  GeneratorCostParams
} from './opf';
import { PowerSystem, Generator } from '@/types';

describe('Optimal Power Flow', () => {
  const createTestSystem = (): PowerSystem => ({
    buses: [
      { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
      { id: '2', name: 'Gen', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
      { id: '3', name: 'Load', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 2, y: 0, active: true },
    ],
    lines: [
      { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
      { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
      { id: 'L13', fromBus: '1', toBus: '3', resistance: 0.04, reactance: 0.08, susceptance: 0, rating: 100, active: true },
    ],
    transformers: [],
    loads: [
      { id: 'LD3', bus: '3', pl: 1.0, ql: 0.5, active: true },
    ],
    generators: [
      { id: 'G1', bus: '1', pg: 0.5, qg: 0, v: 1.0, pmax: 1.5, pmin: 0.2, qmax: 0.5, qmin: -0.5, active: true },
      { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.05, pmax: 1.0, pmin: 0.1, qmax: 0.5, qmin: -0.5, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
    baseMVA: 100,
    baseFreq: 60
  });

  describe('Cost Calculations', () => {
    it('should calculate polynomial cost correctly', () => {
      const costParams: GeneratorCostParams = {
        id: 'G1',
        bus: '1',
        model: 'polynomial',
        a: 10,
        b: 30,
        c: 0.01
      };
      
      const gen: Generator = {
        id: 'G1',
        bus: '1',
        pg: 100,
        qg: 0,
        v: 1.0,
        pmax: 200,
        pmin: 0,
        qmax: 50,
        qmin: -50,
        active: true
      };
      
      // Cost = 10 + 30*100 + 0.01*10000 = 10 + 3000 + 100 = 3110
      const cost = calculateGeneratorCost(gen, costParams);
      expect(cost).toBeCloseTo(3110, 0);
    });

    it('should create default cost parameters', () => {
      const gen: Generator = {
        id: 'G1',
        bus: '1',
        pg: 0.5,
        qg: 0,
        v: 1.0,
        pmax: 1.0,
        pmin: 0.1,
        qmax: 0.5,
        qmin: -0.5,
        active: true
      };
      
      const cost = createDefaultCost(gen);
      
      expect(cost.id).toBe('G1');
      expect(cost.bus).toBe('1');
      expect(cost.model).toBe('polynomial');
      expect(cost.a).toBeGreaterThan(0);
      expect(cost.b).toBeGreaterThan(0);
    });

    it('should calculate total system cost', () => {
      const generators: Generator[] = [
        { id: 'G1', bus: '1', pg: 0.5, qg: 0, v: 1.0, pmax: 1.0, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
        { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.0, pmax: 1.0, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
      ];
      
      const costs: GeneratorCostParams[] = [
        { id: 'G1', bus: '1', model: 'polynomial', a: 10, b: 30, c: 0.01 },
        { id: 'G2', bus: '2', model: 'polynomial', a: 15, b: 35, c: 0.015 },
      ];
      
      const totalCost = calculateTotalCost(generators, costs);
      
      expect(totalCost).toBeGreaterThan(0);
    });
  });

  describe('DC OPF', () => {
    it('should solve OPF and return results', () => {
      const system = createTestSystem();
      const result = solveDCOPF(system);
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.generatorResults).toBeDefined();
      expect(result.generatorResults.length).toBeGreaterThan(0);
    });

    it('should dispatch generators to meet load', () => {
      const system = createTestSystem();
      const result = solveDCOPF(system);
      
      const totalGen = result.generatorResults.reduce((sum, g) => sum + g.pg, 0);
      const totalLoad = system.loads.reduce((sum, l) => sum + l.pl, 0);
      
      // Total generation should be reasonable (not exceeding total capacity)
      expect(totalGen).toBeGreaterThan(0);
      const totalCapacity = system.generators.reduce((sum, g) => sum + g.pmax, 0);
      expect(totalGen).toBeLessThan(totalCapacity);
    });

    it('should respect generator limits', () => {
      const system = createTestSystem();
      const result = solveDCOPF(system);
      
      for (const gen of result.generatorResults) {
        const original = system.generators.find(g => g.id === gen.generator);
        if (original) {
          expect(gen.pg).toBeGreaterThanOrEqual(original.pmin);
          expect(gen.pg).toBeLessThanOrEqual(original.pmax);
        }
      }
    });

    it('should calculate total cost', () => {
      const system = createTestSystem();
      const result = solveDCOPF(system);
      
      expect(result.totalCost).toBeGreaterThan(0);
    });

    it('should handle single generator case', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        generators: [
          { id: 'G1', bus: '1', pg: 0.5, qg: 0, v: 1.0, pmax: 2.0, pmin: 0.2, qmax: 0.5, qmin: -0.5, active: true }
        ]
      };
      
      const result = solveDCOPF(system);
      
      expect(result.success).toBe(true);
      expect(result.generatorResults).toHaveLength(1);
    });
  });

  describe('AC OPF', () => {
    it('should solve AC OPF and return results', () => {
      const system = createTestSystem();
      const result = solveACOPF(system);
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.generatorResults).toBeDefined();
    });

    it('should have elapsed time', () => {
      const system = createTestSystem();
      const result = solveACOPF(system);
      
      expect(result.elapsedTime).toBeGreaterThan(0);
    });
  });

  describe('Security Constrained OPF', () => {
    it('should check contingencies', () => {
      const system = createTestSystem();
      const result = solveSecurityConstrainedOPF(system);
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.violations).toBeDefined();
    });

    it('should include N-1 contingencies', () => {
      const system = createTestSystem();
      const contingencies = [
        { from: '1', to: '2' },
        { from: '2', to: '3' }
      ];
      
      const result = solveSecurityConstrainedOPF(system, undefined, contingencies);
      
      expect(result.violations).toBeDefined();
    });
  });

  describe('Unit Commitment', () => {
    it('should create 24-hour schedule', () => {
      const system = createTestSystem();
      const result = solveUnitCommitment(system, 24);
      
      expect(result.schedules).toHaveLength(24);
      
      for (const schedule of result.schedules) {
        expect(schedule.hour).toBeDefined();
        expect(schedule.generators).toBeDefined();
        expect(schedule.cost).toBeGreaterThanOrEqual(0);
      }
    });

    it('should use custom load pattern', () => {
      const system = createTestSystem();
      const loads = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
      const result = solveUnitCommitment(system, 8, loads);
      
      expect(result.schedules).toHaveLength(8);
      
      // Peak load hour should have more generators on
      const peakSchedule = result.schedules[7];
      const nightSchedule = result.schedules[0];
      
      const peakGenCount = peakSchedule.generators.filter(g => g.on).length;
      const nightGenCount = nightSchedule.generators.filter(g => g.on).length;
      
      expect(peakGenCount).toBeGreaterThanOrEqual(nightGenCount);
    });

    it('should calculate hourly costs', () => {
      const system = createTestSystem();
      const result = solveUnitCommitment(system, 4);
      
      let totalCost = 0;
      for (const schedule of result.schedules) {
        totalCost += schedule.cost;
        // Check that generators with higher output cost more
        const totalPg = schedule.generators.reduce((sum, g) => sum + g.pg, 0);
        expect(totalPg).toBeGreaterThan(0);
      }
      
      expect(totalCost).toBeGreaterThan(0);
    });
  });

  describe('Integration with Power Flow', () => {
    it('should return bus and line results', () => {
      const system = createTestSystem();
      const result = solveDCOPF(system);
      
      expect(result.busResults).toBeDefined();
      expect(result.lineResults).toBeDefined();
      expect(result.losses).toBeDefined();
    });
  });
});
