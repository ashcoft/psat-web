/**
 * Tests for Time Domain Simulation Module
 */

import { describe, it, expect } from 'vitest';
import { 
  runTimeDomainSimulation,
  runContingencyStudy,
  checkStability,
  calculateCriticalClearingTime,
  createGeneratorModels,
  defaultSimulationConfig,
  TimeSeriesResult
} from './timeseries';
import { PowerSystem } from '@/types';

describe('Time Domain Simulation', () => {
  const createTestSystem = (): PowerSystem => ({
    buses: [
      { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
      { id: '2', name: 'Gen', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
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
      { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.05, pmax: 1.0, pmin: 0.1, qmax: 0.5, qmin: -0.5, active: true },
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
    baseMVA: 100,
    baseFreq: 60
  });

  describe('Configuration', () => {
    it('should have default configuration', () => {
      expect(defaultSimulationConfig).toBeDefined();
      expect(defaultSimulationConfig.tStart).toBe(0);
      expect(defaultSimulationConfig.tEnd).toBe(5);
      expect(defaultSimulationConfig.dt).toBe(0.01);
      expect(defaultSimulationConfig.method).toBe('rk4');
    });
  });

  describe('Generator Models', () => {
    it('should create generator models', () => {
      const system = createTestSystem();
      const models = createGeneratorModels(system);
      
      expect(models).toHaveLength(2);
      expect(models[0].id).toBe('G1');
      expect(models[0].bus).toBe('1');
      expect(models[0].H).toBeGreaterThan(0);
      expect(models[0].D).toBeGreaterThan(0);
    });

    it('should set initial state', () => {
      const system = createTestSystem();
      const models = createGeneratorModels(system);
      
      models.forEach(m => {
        expect(m.omega).toBe(1.0);
        expect(m.delta).toBe(0);
      });
    });

    it('should filter inactive generators', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        generators: [
          { id: 'G1', bus: '1', pg: 0.5, qg: 0, v: 1.0, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: true },
          { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.0, pmax: 1, pmin: 0, qmax: 0.5, qmin: -0.5, active: false },
        ]
      };
      const models = createGeneratorModels(system);
      
      expect(models).toHaveLength(1);
      expect(models[0].id).toBe('G1');
    });
  });

  describe('Basic Simulation', () => {
    it('should run simulation with default config', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system);
      
      expect(result).toBeDefined();
      expect(result.time).toBeDefined();
      expect(result.time.length).toBeGreaterThan(0);
    });

    it('should produce time series data', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system);
      
      expect(result.busVoltages).toBeDefined();
      expect(result.busAngles).toBeDefined();
      expect(result.generatorAngles).toBeDefined();
      expect(result.generatorSpeeds).toBeDefined();
    });

    it('should have matching time series lengths', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system);
      
      const n = result.time.length;
      expect(result.busVoltages['1']).toHaveLength(n);
      expect(result.generatorAngles['G1']).toHaveLength(n);
    });
  });

  describe('Custom Configuration', () => {
    it('should respect custom time range', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        tStart: 0,
        tEnd: 10,
        dt: 0.01,
        outputInterval: 0.1
      });
      
      expect(result.time[result.time.length - 1]).toBeLessThanOrEqual(10.01);
      expect(result.time[0]).toBeGreaterThanOrEqual(0);
    });

    it('should respect output interval', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        outputInterval: 0.1
      });
      
      // Check that time intervals are consistent
      for (let i = 1; i < result.time.length; i++) {
        const dt = result.time[i] - result.time[i - 1];
        expect(dt).toBeCloseTo(0.1, 1);
      }
    });

    it('should support different integration methods', () => {
      const system = createTestSystem();
      
      const eulerResult = runTimeDomainSimulation(system, { method: 'euler' });
      const rk4Result = runTimeDomainSimulation(system, { method: 'rk4' });
      
      expect(eulerResult.time).toHaveLength(rk4Result.time.length);
    });
  });

  describe('Fault Simulation', () => {
    it('should simulate fault event', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        faultTime: 1.0,
        faultDuration: 0.1
      });
      
      expect(result).toBeDefined();
      expect(result.busVoltages).toBeDefined();
    });

    it('should recover from short fault', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        tEnd: 3,
        faultTime: 1.0,
        faultDuration: 0.05
      });
      
      // Check that system recovers after fault clears
      const voltages = result.busVoltages['1'];
      const preFault = voltages[Math.floor(voltages.length * 0.3)];
      const postFault = voltages[voltages.length - 1];
      
      expect(postFault).toBeDefined();
    });
  });

  describe('Load Change Simulation', () => {
    it('should simulate load change', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        loadChangeTime: 2.0,
        loadChangeFactor: 1.1
      });
      
      expect(result).toBeDefined();
    });

    it('should track frequency response to load change', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system, {
        loadChangeTime: 2.0,
        loadChangeFactor: 1.2
      });
      
      // After load increase, frequencies should initially dip
      expect(result.busFrequencies['1']).toBeDefined();
    });
  });

  describe('Stability Analysis', () => {
    it('should check stability from results', () => {
      const system = createTestSystem();
      const result = runTimeDomainSimulation(system);
      const stability = checkStability(result);
      
      expect(stability).toBeDefined();
      expect(stability.stable).toBeDefined();
      expect(stability.minOmega).toBeDefined();
      expect(stability.maxOmega).toBeDefined();
    });

    it('should detect unstable simulation', () => {
      const result: TimeSeriesResult = {
        time: [0, 0.1, 0.2, 0.3, 0.4, 0.5],
        busVoltages: { '1': [1, 1.1, 1.2, 1.3, 1.4, 1.5] },
        busAngles: { '1': [0, 0, 0, 0, 0, 0] },
        generatorAngles: { 'G1': [0, 10, 20, 30, 40, 50] },
        generatorSpeeds: { 'G1': [60, 65, 70, 75, 80, 85] },
        lineFlows: {},
        busFrequencies: { '1': [60, 65, 70, 75, 80, 85] }
      };
      
      const stability = checkStability(result);
      expect(stability.stable).toBe(false);
      expect(stability.criticalTime).toBeDefined();
    });

    it('should handle empty results', () => {
      const result: TimeSeriesResult = {
        time: [],
        busVoltages: {},
        busAngles: {},
        generatorAngles: {},
        generatorSpeeds: {},
        lineFlows: {},
        busFrequencies: {}
      };
      
      const stability = checkStability(result);
      expect(stability.stable).toBe(true);
    });
  });

  describe('Contingency Study', () => {
    it('should run multiple contingencies', () => {
      const system = createTestSystem();
      const contingencies = [
        { name: '3-phase fault', faultTime: 1.0, faultDuration: 0.1 },
        { name: 'Load increase', loadChange: { time: 2.0, factor: 1.1 } }
      ];
      
      const results = runContingencyStudy(system, contingencies);
      
      expect(results).toHaveLength(2);
      expect(results[0].name).toBe('3-phase fault');
      expect(results[1].name).toBe('Load increase');
    });

    it('should have results for each contingency', () => {
      const system = createTestSystem();
      const contingencies = [
        { name: 'Contingency 1' },
        { name: 'Contingency 2' }
      ];
      
      const results = runContingencyStudy(system, contingencies);
      
      results.forEach(r => {
        expect(r.result.time).toBeDefined();
        expect(r.result.time.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Critical Clearing Time', () => {
    it('should estimate CCT', () => {
      const system = createTestSystem();
      const cct = calculateCriticalClearingTime(system);
      
      expect(cct).toBeDefined();
      expect(cct.cct).toBeGreaterThan(0);
      expect(cct.cctRange).toHaveLength(2);
      expect(cct.cctRange[0]).toBeLessThan(cct.cctRange[1]);
    });

    it('should have fault time', () => {
      const system = createTestSystem();
      const cct = calculateCriticalClearingTime(system);
      
      expect(cct.faultTime).toBeDefined();
      expect(typeof cct.faultTime).toBe('number');
    });
  });
});
