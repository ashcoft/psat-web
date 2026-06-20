/**
 * Tests for Fault Analysis Module
 */

import { describe, it, expect } from 'vitest';
import { 
  calculateThreePhaseFault,
  calculateLineToGroundFault,
  calculateLineToLineFault,
  calculateDoubleLineToGroundFault,
  performFaultStudy,
  calculateAllBusFaultCurrents,
  calculateRelayCoordination
} from './fault';
import { PowerSystem } from '@/types';

describe('Fault Analysis', () => {
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
    ],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '1' }],
    baseMVA: 100,
    baseFreq: 60
  });

  describe('Three-Phase Fault', () => {
    it('should calculate three-phase fault current', () => {
      const system = createTestSystem();
      const result = calculateThreePhaseFault(system, '1');
      
      expect(result).toBeDefined();
      expect(result.faultType).toBe('three-phase');
      expect(result.faultBus).toBe('1');
      expect(result.faultCurrent).toBeGreaterThan(0);
    });

    it('should have symmetrical components', () => {
      const system = createTestSystem();
      const result = calculateThreePhaseFault(system, '2');
      
      expect(result.symmetricalComponents).toBeDefined();
      expect(result.symmetricalComponents?.I1).toBe(result.faultCurrent);
      expect(result.symmetricalComponents?.I2).toBe(0);
      expect(result.symmetricalComponents?.I0).toBe(0);
    });

    it('should calculate fault MVA', () => {
      const system = createTestSystem();
      const result = calculateThreePhaseFault(system, '3');
      
      expect(result.faultMVA).toBeGreaterThan(0);
    });

    it('should handle non-existent bus', () => {
      const system = createTestSystem();
      
      expect(() => calculateThreePhaseFault(system, '999')).toThrow();
    });
  });

  describe('Line-to-Ground Fault', () => {
    it('should calculate L-G fault current', () => {
      const system = createTestSystem();
      const result = calculateLineToGroundFault(system, '2');
      
      expect(result).toBeDefined();
      expect(result.faultType).toBe('line-to-ground');
      expect(result.faultCurrent).toBeGreaterThan(0);
    });

    it('should have zero sequence component', () => {
      const system = createTestSystem();
      const result = calculateLineToGroundFault(system, '1');
      
      expect(result.symmetricalComponents?.I0).toBeDefined();
    });

    it('should handle fault resistance', () => {
      const system = createTestSystem();
      const result = calculateLineToGroundFault(system, '3', 0.1);
      
      expect(result).toBeDefined();
      expect(result.faultCurrent).toBeLessThan(
        calculateLineToGroundFault(system, '3', 0).faultCurrent
      );
    });
  });

  describe('Line-to-Line Fault', () => {
    it('should calculate L-L fault current', () => {
      const system = createTestSystem();
      const result = calculateLineToLineFault(system, '2');
      
      expect(result).toBeDefined();
      expect(result.faultType).toBe('line-to-line');
      expect(result.faultCurrent).toBeGreaterThan(0);
    });

    it('should have no zero sequence', () => {
      const system = createTestSystem();
      const result = calculateLineToLineFault(system, '1');
      
      expect(result.symmetricalComponents?.I0).toBe(0);
    });

    it('should have equal magnitude I2 as I1', () => {
      const system = createTestSystem();
      const result = calculateLineToLineFault(system, '3');
      
      expect(Math.abs(result.symmetricalComponents?.I1 || 0)).toBeCloseTo(
        Math.abs(result.symmetricalComponents?.I2 || 0),
        5
      );
    });
  });

  describe('Double Line-to-Ground Fault', () => {
    it('should calculate DLG fault current', () => {
      const system = createTestSystem();
      const result = calculateDoubleLineToGroundFault(system, '2');
      
      expect(result).toBeDefined();
      expect(result.faultType).toBe('double-line-to-ground');
      expect(result.faultCurrent).toBeGreaterThan(0);
    });

    it('should have all sequence components', () => {
      const system = createTestSystem();
      const result = calculateDoubleLineToGroundFault(system, '1');
      
      expect(result.symmetricalComponents?.I0).toBeDefined();
      expect(result.symmetricalComponents?.I1).toBeDefined();
      expect(result.symmetricalComponents?.I2).toBeDefined();
    });
  });

  describe('Complete Fault Study', () => {
    it('should perform fault study', () => {
      const system = createTestSystem();
      const result = performFaultStudy(system);
      
      expect(result).toBeDefined();
      expect(result.threePhaseFaults).toBeDefined();
      expect(result.lineToGroundFaults).toBeDefined();
    });

    it('should calculate faults at all buses', () => {
      const system = createTestSystem();
      const result = performFaultStudy(system);
      
      expect(result.threePhaseFaults.length).toBeGreaterThan(0);
      expect(result.lineToGroundFaults.length).toBeGreaterThan(0);
    });

    it('should calculate protective device requirements', () => {
      const system = createTestSystem();
      const result = performFaultStudy(system);
      
      expect(result.protectiveDeviceRequirements).toBeDefined();
      expect(result.protectiveDeviceRequirements.length).toBeGreaterThan(0);
    });

    it('should include breaker ratings', () => {
      const system = createTestSystem();
      const result = performFaultStudy(system);
      
      result.protectiveDeviceRequirements.forEach(req => {
        expect(req.minBreakerRating).toBeGreaterThan(0);
        expect(req.recommendedBreakerRating).toBeGreaterThan(req.minBreakerRating);
      });
    });

    it('should include relay settings', () => {
      const system = createTestSystem();
      const result = performFaultStudy(system);
      
      result.protectiveDeviceRequirements.forEach(req => {
        expect(req.relaySettings).toBeDefined();
        expect(req.relaySettings.pickup).toBeGreaterThan(0);
        expect(req.relaySettings.timeDelay).toBeGreaterThanOrEqual(0);
      });
    });
  });

  describe('All Bus Fault Currents', () => {
    it('should calculate fault currents for all buses', () => {
      const system = createTestSystem();
      const results = calculateAllBusFaultCurrents(system, 'three-phase');
      
      expect(results.length).toBeGreaterThan(0);
    });

    it('should sort by MVA descending', () => {
      const system = createTestSystem();
      const results = calculateAllBusFaultCurrents(system, 'three-phase');
      
      for (let i = 1; i < results.length; i++) {
        expect(results[i - 1].mva).toBeGreaterThanOrEqual(results[i].mva);
      }
    });

    it('should work for all fault types', () => {
      const system = createTestSystem();
      
      expect(calculateAllBusFaultCurrents(system, 'three-phase').length).toBeGreaterThan(0);
      expect(calculateAllBusFaultCurrents(system, 'line-to-ground').length).toBeGreaterThan(0);
      expect(calculateAllBusFaultCurrents(system, 'line-to-line').length).toBeGreaterThan(0);
      expect(calculateAllBusFaultCurrents(system, 'double-line-to-ground').length).toBeGreaterThan(0);
    });
  });

  describe('Relay Coordination', () => {
    it('should calculate coordination times', () => {
      const result = calculateRelayCoordination();
      
      expect(result).toBeDefined();
      expect(result.upstream).toBeDefined();
      expect(result.downstream).toBeDefined();
      expect(result.coordinationTime).toBeGreaterThan(0);
    });

    it('should have upstream slower than downstream', () => {
      const result = calculateRelayCoordination();
      
      expect(result.upstream.time).toBeGreaterThan(result.downstream.time);
    });
  });
});
