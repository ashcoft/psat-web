/**
 * Tests for Small Signal Stability Analysis Module
 */

import { describe, it, expect } from 'vitest';
import { 
  analyzeSmallSignalStability,
  calculateParticipationFactors,
  checkModeStability,
  filterModesByFrequency,
  filterModesByType,
  calculateDampingTorque,
  getModalSummary,
  buildStateMatrix
} from './stability';
import { PowerSystem } from '@/types';

describe('Small Signal Stability Analysis', () => {
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

  describe('State Matrix Building', () => {
    it('should build state matrix for multi-machine system', () => {
      const system = createTestSystem();
      const network = buildStateMatrix(system);
      
      expect(network.n).toBe(2);
      expect(network.M).toHaveLength(2);
      expect(network.D).toHaveLength(2);
      expect(network.K).toHaveLength(2);
    });

    it('should have positive inertia values', () => {
      const system = createTestSystem();
      const network = buildStateMatrix(system);
      
      for (let i = 0; i < network.n; i++) {
        expect(network.M[i][i]).toBeGreaterThan(0);
      }
    });

    it('should handle system with no generators', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        generators: []
      };
      const network = buildStateMatrix(system);
      
      expect(network.n).toBe(0);
    });
  });

  describe('Eigenvalue Analysis', () => {
    it('should compute eigenvalues for test system', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      expect(result).toBeDefined();
      expect(result.eigenvalues).toBeDefined();
    });

    it('should identify all eigenvalue properties', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      result.eigenvalues.forEach(ev => {
        expect(ev.eigenvalue).toBeDefined();
        expect(ev.dampingRatio).toBeDefined();
        expect(ev.frequency).toBeDefined();
        expect(ev.modeType).toBeDefined();
        expect(ev.damping).toBeDefined();
      });
    });

    it('should have correct damping classifications', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      result.eigenvalues.forEach(ev => {
        expect(['stable', 'poorly_damped', 'unstable']).toContain(ev.damping);
      });
    });

    it('should have correct mode type classifications', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      result.eigenvalues.forEach(ev => {
        expect(['swing', 'local', 'interarea', 'control', 'torsional']).toContain(ev.modeType);
      });
    });
  });

  describe('System Damping Assessment', () => {
    it('should classify system damping', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      expect(['good', 'marginal', 'poor', 'unstable']).toContain(result.systemDamping);
    });

    it('should identify unstable modes', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      result.unstableModes.forEach(mode => {
        expect(mode.damping).toBe('unstable');
        expect(mode.eigenvalue.real).toBeGreaterThan(0);
      });
    });

    it('should identify poorly damped modes', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      
      result.criticallyDampedModes.forEach(mode => {
        expect(mode.damping).toBe('poorly_damped');
      });
    });
  });

  describe('Participation Factors', () => {
    it('should calculate participation factors', () => {
      const system = createTestSystem();
      const factors = calculateParticipationFactors(system);
      
      expect(factors).toBeDefined();
      expect(Array.isArray(factors)).toBe(true);
    });

    it('should have factors for each state variable', () => {
      const system = createTestSystem();
      const factors = calculateParticipationFactors(system);
      
      // Should have 4 state variables for 2-machine system (2 delta, 2 omega)
      expect(factors.length).toBe(4);
    });

    it('should handle system with no generators', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        generators: []
      };
      const factors = calculateParticipationFactors(system);
      
      expect(factors).toHaveLength(0);
    });
  });

  describe('Mode Filtering', () => {
    it('should filter modes by frequency range', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      const localModes = filterModesByFrequency(result, 0.1, 0.8);
      
      localModes.forEach(mode => {
        expect(mode.frequency).toBeGreaterThanOrEqual(0.1);
        expect(mode.frequency).toBeLessThanOrEqual(0.8);
      });
    });

    it('should filter modes by type', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      const localModes = filterModesByType(result, 'local');
      
      localModes.forEach(mode => {
        expect(mode.modeType).toBe('local');
      });
    });

    it('should return empty array for no matches', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        generators: []
      };
      const result = analyzeSmallSignalStability(system);
      const modes = filterModesByFrequency(result, 0.1, 0.8);
      
      expect(modes).toHaveLength(0);
    });
  });

  describe('Mode Stability Check', () => {
    it('should classify stable modes', () => {
      expect(checkModeStability(0.5, 0.1)).toBe('stable');
      expect(checkModeStability(1.0, 0.2)).toBe('stable');
    });

    it('should classify marginal modes', () => {
      expect(checkModeStability(0.5, 0.03)).toBe('marginal');
    });

    it('should classify unstable modes', () => {
      expect(checkModeStability(0.5, -0.1)).toBe('unstable');
    });
  });

  describe('Damping Torque Calculation', () => {
    it('should calculate damping torque', () => {
      const torque = calculateDampingTorque(2.0, 1.01);
      expect(torque).toBeCloseTo(0.02, 3);
    });

    it('should return zero at synchronous speed', () => {
      const torque = calculateDampingTorque(2.0, 1.0);
      expect(torque).toBe(0);
    });
  });

  describe('Modal Summary', () => {
    it('should generate modal summary', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      const { summary, recommendations } = getModalSummary(result);
      
      expect(summary).toBeDefined();
      expect(typeof summary).toBe('string');
      expect(recommendations).toBeDefined();
      expect(Array.isArray(recommendations)).toBe(true);
    });

    it('should include recommendations for unstable system', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      const { recommendations } = getModalSummary(result);
      
      // Should have at least one recommendation
      expect(recommendations.length).toBeGreaterThan(0);
    });

    it('should mention unstable modes in recommendations', () => {
      const system = createTestSystem();
      const result = analyzeSmallSignalStability(system);
      const { recommendations } = getModalSummary(result);
      
      // If there are unstable modes, should mention them
      if (result.unstableModes.length > 0) {
        const hasUnstableRec = recommendations.some(r => 
          r.toLowerCase().includes('unstable')
        );
        expect(hasUnstableRec).toBe(true);
      }
    });
  });

  describe('Large System', () => {
    it('should handle system with multiple generators', () => {
      const system: PowerSystem = {
        ...createTestSystem(),
        buses: [
          { id: '1', name: 'Slack', type: 'slack', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 0, y: 0, active: true },
          { id: '2', name: 'Gen1', type: 'pv', voltage: 1.05, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 1, y: 0, active: true },
          { id: '3', name: 'Gen2', type: 'pv', voltage: 1.02, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 2, y: 0, active: true },
          { id: '4', name: 'Load', type: 'pq', voltage: 1.0, angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1, x: 3, y: 0, active: true },
        ],
        generators: [
          { id: 'G1', bus: '1', pg: 0.8, qg: 0, v: 1.0, pmax: 1.5, pmin: 0.2, qmax: 0.5, qmin: -0.5, active: true },
          { id: 'G2', bus: '2', pg: 0.5, qg: 0, v: 1.05, pmax: 1.0, pmin: 0.1, qmax: 0.5, qmin: -0.5, active: true },
          { id: 'G3', bus: '3', pg: 0.3, qg: 0, v: 1.02, pmax: 1.0, pmin: 0.1, qmax: 0.5, qmin: -0.5, active: true },
        ],
        lines: [
          { id: 'L12', fromBus: '1', toBus: '2', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
          { id: 'L23', fromBus: '2', toBus: '3', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
          { id: 'L34', fromBus: '3', toBus: '4', resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true },
        ],
        loads: [
          { id: 'LD4', bus: '4', pl: 1.5, ql: 0.5, active: true },
        ]
      };
      
      const result = analyzeSmallSignalStability(system);
      
      expect(result.eigenvalues.length).toBeGreaterThan(0);
      expect(result.systemDamping).toBeDefined();
    });
  });
});
