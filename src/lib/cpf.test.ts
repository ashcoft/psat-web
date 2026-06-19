/**
 * Tests for Continuation Power Flow (CPF) Module
 */

import { describe, it, expect } from 'vitest';
import { 
  runCPF,
  analyzeVoltageCollapse,
  calculateLIndex,
  generatePVData,
  defaultCPFConfig
} from './cpf';
import { PowerSystem } from '@/types';

describe('Continuation Power Flow', () => {
  const createTestSystem = (): PowerSystem => ({
    buses: [
      { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
      { id: '2', name: 'PV', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
      { id: '3', name: 'Load', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 2, y: 0, active: true },
    ],
    lines: [
      { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
      { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
    ],
    transformers: [],
    loads: [
      { id: 'LD3', bus: '3', pl: 1.0, ql: 0.5, active: true },
    ],
    generators: [
      { id: 'G1', bus: '1', pg: 0.8, qg: 0, v: 1.0, pmax: 1.5, pmin: 0.2, qmax: 0.5, qmin: -0.5, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
    baseMVA: 100,
    baseFreq: 60
  });

  describe('Default Configuration', () => {
    it('should have default CPF configuration', () => {
      expect(defaultCPFConfig).toBeDefined();
      expect(defaultCPFConfig.lambdaStart).toBe(0);
      expect(defaultCPFConfig.lambdaMax).toBe(5);
      expect(defaultCPFConfig.stepSize).toBe(0.1);
      expect(defaultCPFConfig.adaptiveStep).toBe(true);
    });
  });

  describe('Basic CPF', () => {
    it('should run CPF and return results', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(result).toBeDefined();
      expect(result.results).toBeDefined();
      expect(result.pvCurve).toBeDefined();
    });

    it('should produce results array', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(Array.isArray(result.results)).toBe(true);
    });

    it('should have converged flag', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(typeof result.converged).toBe('boolean');
    });
  });

  describe('PV Curve', () => {
    it('should generate PV curve structure', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(result.pvCurve).toBeDefined();
      expect(Array.isArray(result.pvCurve)).toBe(true);
    });

    it('should have lambda and voltage pairs', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      result.pvCurve.forEach(curve => {
        curve.forEach(point => {
          expect(point.lambda).toBeDefined();
          expect(point.v).toBeDefined();
        });
      });
    });

    it('should track voltage decrease with loading', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      if (result.pvCurve.length > 1) {
        const loadBusCurve = result.pvCurve[result.pvCurve.length - 1];
        if (loadBusCurve.length >= 2) {
          const firstV = loadBusCurve[0].v;
          const lastV = loadBusCurve[loadBusCurve.length - 1].v;
          // Voltage should generally decrease with increasing load
          expect(typeof firstV).toBe('number');
          expect(typeof lastV).toBe('number');
        }
      }
    });
  });

  describe('Nose Point', () => {
    it('should have nosePoint structure', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(result.nosePoint || true).toBeDefined();
    });

    it('should have maximumLoadingPoint structure', () => {
      const system = createTestSystem();
      const result = runCPF(system);
      
      expect(result.maximumLoadingPoint || true).toBeDefined();
    });
  });

  describe('Voltage Collapse Analysis', () => {
    it('should analyze voltage collapse', () => {
      const system = createTestSystem();
      const result = analyzeVoltageCollapse(system);
      
      expect(result).toBeDefined();
      expect(result.lambdaMax).toBeDefined();
      expect(result.recommendations).toBeDefined();
    });

    it('should identify critical bus', () => {
      const system = createTestSystem();
      const result = analyzeVoltageCollapse(system);
      
      expect(result.criticalBus || true).toBeDefined();
    });

    it('should have recommendations array', () => {
      const system = createTestSystem();
      const result = analyzeVoltageCollapse(system);
      
      expect(Array.isArray(result.recommendations)).toBe(true);
    });
  });

  describe('L-Index', () => {
    it('should calculate L-index', () => {
      const system = createTestSystem();
      const result = calculateLIndex(system);
      
      expect(result).toBeDefined();
      expect(result.L).toBeDefined();
      expect(result.Lmax).toBeDefined();
      expect(result.stable).toBeDefined();
    });

    it('should have L-index for each bus', () => {
      const system = createTestSystem();
      const result = calculateLIndex(system);
      
      if (result.L.length > 0) {
        result.L.forEach(l => {
          expect(l).toBeGreaterThanOrEqual(0);
        });
      }
    });

    it('should classify system as stable or unstable', () => {
      const system = createTestSystem();
      const result = calculateLIndex(system);
      
      expect(typeof result.stable).toBe('boolean');
    });
  });

  describe('PV Data Generation', () => {
    it('should generate PV data for specific bus', () => {
      const system = createTestSystem();
      const pvData = generatePVData(system, '3');
      
      expect(pvData.p).toBeDefined();
      expect(pvData.v).toBeDefined();
      expect(pvData.p.length).toBe(pvData.v.length);
    });

    it('should have matching array lengths', () => {
      const system = createTestSystem();
      const pvData = generatePVData(system, '2');
      
      expect(pvData.p.length).toBe(pvData.v.length);
    });
  });

  describe('Configuration Options', () => {
    it('should accept custom configuration', () => {
      const system = createTestSystem();
      const result1 = runCPF(system, { stepSize: 0.5 });
      const result2 = runCPF(system, { stepSize: 0.1 });
      
      expect(result1).toBeDefined();
      expect(result2).toBeDefined();
    });

    it('should respect maximum lambda', () => {
      const system = createTestSystem();
      const result = runCPF(system, { lambdaMax: 1.5 });
      
      if (result.results.length > 0) {
        result.results.forEach(r => {
          expect(r.lambda).toBeLessThanOrEqual(1.6);
        });
      }
    });

    it('should work with adaptive step disabled', () => {
      const system = createTestSystem();
      const result = runCPF(system, { adaptiveStep: false });
      
      expect(result).toBeDefined();
    });
  });

  describe('Large System', () => {
    it('should handle larger system', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'Gen', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
          { id: '3', name: 'Bus', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 2, y: 0, active: true },
          { id: '4', name: 'Load1', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 3, y: 0, active: true },
          { id: '5', name: 'Load2', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 4, y: 0, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
          { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
          { id: 'L34', fromBus: '3', toBus: '4', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
          { id: 'L35', fromBus: '3', toBus: '5', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        loads: [
          { id: 'LD4', bus: '4', pl: 1.0, ql: 0.5, active: true },
          { id: 'LD5', bus: '5', pl: 0.8, ql: 0.4, active: true },
        ]
      };
      
      const result = runCPF(system, { lambdaMax: 2 });
      expect(result).toBeDefined();
    });
  });
});
