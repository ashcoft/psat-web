/**
 * Comprehensive Tests for Power System Types and IEC Symbols
 */

import { describe, it, expect } from 'vitest';
import {
  symbols,
  getSymbol,
  getSymbolsByCategory,
  symbolCategories,
  renderSymbol,
} from './symbols';
import type { IECSymbolType, PowerSystem, Bus, Line, Transformer, Generator, Load } from '@/types';

describe('IEC Symbol Library', () => {
  describe('All required symbols exist', () => {
    const requiredSymbols: IECSymbolType[] = [
      'bus',
      'generator',
      'load',
      'motor',
      'line',
      'transformer',
      'transformer-3w',
      'transformer-reg',
      'breaker',
      'switch',
      'disconnect',
      'fuse',
      'sectionalizer',
      'recloser',
      'current-transformer',
      'potential-transformer',
      'relay',
      'meter',
      'ground',
      'external-grid',
      'equivalent',
      'svc',
      'statcom',
      'tcsc',
      'upfc',
      'wind-turbine',
      'pv-array',
      'battery',
      'substation',
      'busbar',
      'shunt',
      'capacitor',
      'capacitor-bank',
      'consortium',
      'arrestor',
      'junction',
    ];

    requiredSymbols.forEach((type) => {
      it(`should have symbol for ${type}`, () => {
        const symbol = getSymbol(type);
        expect(symbol).toBeDefined();
        expect(symbol.name).toBeDefined();
        expect(symbol.category).toBeDefined();
        expect(symbol.width).toBeGreaterThan(0);
        expect(symbol.height).toBeGreaterThan(0);
        expect(symbol.connectionPoints).toBeDefined();
        expect(symbol.connectionPoints.length).toBeGreaterThan(0);
        expect(symbol.properties).toBeDefined();
        expect(symbol.properties.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Symbol properties validation', () => {
    it('should have all required properties for generator symbol', () => {
      const gen = getSymbol('generator');
      const propKeys = gen.properties.map((p) => p.key);
      expect(propKeys).toContain('pg');
      expect(propKeys).toContain('qg');
      expect(propKeys).toContain('v');
      expect(propKeys).toContain('pmax');
      expect(propKeys).toContain('pmin');
      expect(propKeys).toContain('qmax');
      expect(propKeys).toContain('qmin');
    });

    it('should have all required properties for load symbol', () => {
      const load = getSymbol('load');
      const propKeys = load.properties.map((p) => p.key);
      expect(propKeys).toContain('pl');
      expect(propKeys).toContain('ql');
      expect(propKeys).toContain('demandModel');
    });

    it('should have all required properties for transformer symbol', () => {
      const tx = getSymbol('transformer');
      const propKeys = tx.properties.map((p) => p.key);
      expect(propKeys).toContain('r');
      expect(propKeys).toContain('x');
      expect(propKeys).toContain('tap');
      expect(propKeys).toContain('rating');
      expect(propKeys).toContain('vectorGroup');
    });

    it('should have all required properties for line symbol', () => {
      const line = getSymbol('line');
      const propKeys = line.properties.map((p) => p.key);
      expect(propKeys).toContain('r');
      expect(propKeys).toContain('x');
      expect(propKeys).toContain('b');
      expect(propKeys).toContain('rating');
    });

    it('should have FACTS device properties', () => {
      const svc = getSymbol('svc');
      const svcKeys = svc.properties.map((p) => p.key);
      expect(svcKeys).toContain('qMax');
      expect(svcKeys).toContain('qMin');
      expect(svcKeys).toContain('vRef');

      const statcom = getSymbol('statcom');
      const statcomKeys = statcom.properties.map((p) => p.key);
      expect(statcomKeys).toContain('vdc');
    });

    it('should have renewable energy properties', () => {
      const wind = getSymbol('wind-turbine');
      const windKeys = wind.properties.map((p) => p.key);
      expect(windKeys).toContain('pmax');
      expect(windKeys).toContain('wsCutIn');
      expect(windKeys).toContain('wsRated');
      expect(windKeys).toContain('wsCutOut');

      const pv = getSymbol('pv-array');
      const pvKeys = pv.properties.map((p) => p.key);
      expect(pvKeys).toContain('pmax');
    });

    it('should have battery storage properties', () => {
      const batt = getSymbol('battery');
      const battKeys = batt.properties.map((p) => p.key);
      expect(battKeys).toContain('eMax');
      expect(battKeys).toContain('pMax');
      expect(battKeys).toContain('eMin');
      expect(battKeys).toContain('socInitial');
      expect(battKeys).toContain('etaCharge');
      expect(battKeys).toContain('etaDischarge');
    });
  });

  describe('Symbol categories', () => {
    it('should have all required categories', () => {
      const categories = Object.keys(symbolCategories);
      expect(categories).toContain('generation');
      expect(categories).toContain('load');
      expect(categories).toContain('transmission');
      expect(categories).toContain('distribution');
      expect(categories).toContain('protection');
      expect(categories).toContain('measurement');
      expect(categories).toContain('compensation');
      expect(categories).toContain('storage');
      expect(categories).toContain('renewable');
      expect(categories).toContain('substation');
      expect(categories).toContain('network');
    });

    it('should have generators in generation category', () => {
      const genSymbols = getSymbolsByCategory('generation');
      expect(genSymbols.length).toBeGreaterThan(0);
      const types = genSymbols.map((s) => s.type);
      expect(types).toContain('generator');
    });

    it('should have loads in load category', () => {
      const loadSymbols = getSymbolsByCategory('load');
      expect(loadSymbols.length).toBeGreaterThan(0);
    });

    it('should have protection devices in protection category', () => {
      const protSymbols = getSymbolsByCategory('protection');
      expect(protSymbols.length).toBeGreaterThan(0);
      const types = protSymbols.map((s) => s.type);
      expect(types).toContain('breaker');
      expect(types).toContain('fuse');
    });

    it('should have compensation devices in compensation category', () => {
      const compSymbols = getSymbolsByCategory('compensation');
      expect(compSymbols.length).toBeGreaterThan(0);
      const types = compSymbols.map((s) => s.type);
      expect(types).toContain('svc');
      expect(types).toContain('statcom');
    });
  });

  describe('Symbol connection points', () => {
    it('should have valid connection points for bus', () => {
      const bus = getSymbol('bus');
      expect(bus.connectionPoints).toHaveLength(4);
      const types = bus.connectionPoints.map((p) => p.type);
      expect(types).toContain('top');
      expect(types).toContain('bottom');
      expect(types).toContain('left');
      expect(types).toContain('right');
    });

    it('should have valid connection points for transformer', () => {
      const tx = getSymbol('transformer');
      expect(tx.connectionPoints).toHaveLength(2);
      const types = tx.connectionPoints.map((p) => p.type);
      expect(types).toContain('top');
      expect(types).toContain('bottom');
    });

    it('should have valid connection points for three-winding transformer', () => {
      const tx3 = getSymbol('transformer-3w');
      expect(tx3.connectionPoints).toHaveLength(3);
      const types = tx3.connectionPoints.map((p) => p.type);
      expect(types).toContain('top');
      expect(types).toContain('left');
      expect(types).toContain('right');
    });

    it('should have valid connection points for breaker', () => {
      const brk = getSymbol('breaker');
      expect(brk.connectionPoints).toHaveLength(2);
      const types = brk.connectionPoints.map((p) => p.type);
      expect(types).toContain('left');
      expect(types).toContain('right');
    });
  });

  describe('Symbol dimensions', () => {
    it('should have reasonable dimensions for all symbols', () => {
      Object.values(symbols).forEach((symbol) => {
        expect(symbol.width).toBeGreaterThan(0);
        expect(symbol.width).toBeLessThanOrEqual(100);
        expect(symbol.height).toBeGreaterThan(0);
        expect(symbol.height).toBeLessThanOrEqual(100);
      });
    });

    it('should have larger dimensions for substation', () => {
      const sub = getSymbol('substation');
      expect(sub.width).toBeGreaterThanOrEqual(50);
      expect(sub.height).toBeGreaterThanOrEqual(50);
    });
  });

  describe('Symbol rendering', () => {
    it('should have render function for all symbols', () => {
      Object.values(symbols).forEach((symbol) => {
        expect(typeof symbol.render).toBe('function');
      });
    });

    // Note: Canvas rendering tests are skipped as jsdom doesn't fully support Canvas API
    // These tests should be run in a browser environment or with a proper canvas mock
    it.skip('should render without throwing (requires canvas mock)', () => {
      const canvas = document.createElement('canvas');
      canvas.width = 200;
      canvas.height = 200;
      const ctx = canvas.getContext('2d');
      if (!ctx) throw new Error('Could not get canvas context');

      Object.entries(symbols).forEach(([type, symbol]) => {
        expect(() => {
          symbol.render(ctx, 100, 100, 0);
        }).not.toThrow();
      });
    });
  });
});

describe('Power System Types', () => {
  describe('Bus types', () => {
    it('should support all bus types', () => {
      const busTypes: Bus['type'][] = ['slack', 'pv', 'pq', 'isolated'];
      busTypes.forEach((type) => {
        const bus: Bus = {
          id: 'bus1',
          name: 'Test Bus',
          type,
          voltage: 1.0,
          angle: 0,
          vmin: 0.9,
          vmax: 1.1,
          area: 1,
          region: 1,
          x: 0,
          y: 0,
          active: true,
        };
        expect(bus.type).toBe(type);
      });
    });

    it('should support extended bus properties', () => {
      const bus: Bus = {
        id: 'bus1',
        name: 'Test Bus',
        type: 'pq',
        voltage: 1.0,
        angle: 0,
        vmin: 0.9,
        vmax: 1.1,
        area: 1,
        region: 1,
        x: 0,
        y: 0,
        active: true,
        vScheduled: 1.0,
        vbase: 138,
        zone: 1,
        owner: 1,
        comments: 'Test bus',
      };
      expect(bus.vScheduled).toBe(1.0);
      expect(bus.vbase).toBe(138);
      expect(bus.zone).toBe(1);
      expect(bus.owner).toBe(1);
      expect(bus.comments).toBe('Test bus');
    });
  });

  describe('Line properties', () => {
    it('should support all line types', () => {
      const lineTypes: Line['lineType'][] = ['overhead', 'underground', 'cable', 'tunnel'];
      lineTypes.forEach((lineType) => {
        const line: Line = {
          id: 'line1',
          name: 'Test Line',
          fromBus: 'bus1',
          toBus: 'bus2',
          resistance: 0.01,
          reactance: 0.04,
          susceptance: 0,
          rating: 100,
          active: true,
          lineType,
        };
        expect(line.lineType).toBe(lineType);
      });
    });

    it('should support emergency ratings', () => {
      const line: Line = {
        id: 'line1',
        fromBus: 'bus1',
        toBus: 'bus2',
        resistance: 0.01,
        reactance: 0.04,
        susceptance: 0,
        rating: 100,
        ratingA: 120,
        ratingB: 150,
        active: true,
      };
      expect(line.rating).toBe(100);
      expect(line.ratingA).toBe(120);
      expect(line.ratingB).toBe(150);
    });
  });

  describe('Transformer properties', () => {
    it('should support vector groups', () => {
      const vectorGroups: Transformer['vectorGroup'][] = [
        'Yy0', 'Yy6', 'Dy1', 'Dy11', 'Dy5', 'Dy7', 'Yy4', 'Yy8',
      ];
      vectorGroups.forEach((vg) => {
        const tx: Transformer = {
          id: 'tx1',
          name: 'Test Transformer',
          fromBus: 'bus1',
          toBus: 'bus2',
          resistance: 0.01,
          reactance: 0.06,
          tap: 1.0,
          shift: 0,
          rating: 100,
          active: true,
          vectorGroup: vg,
        };
        expect(tx.vectorGroup).toBe(vg);
      });
    });

    it('should support transformer connections', () => {
      const connections: Transformer['connection'][] = ['wye', 'delta', 'zigzag'];
      connections.forEach((conn) => {
        const tx: Transformer = {
          id: 'tx1',
          fromBus: 'bus1',
          toBus: 'bus2',
          resistance: 0.01,
          reactance: 0.06,
          tap: 1.0,
          shift: 0,
          rating: 100,
          active: true,
          connection: conn,
        };
        expect(tx.connection).toBe(conn);
      });
    });
  });

  describe('Generator properties', () => {
    it('should support polynomial cost model', () => {
      const gen: Generator = {
        id: 'gen1',
        name: 'Test Generator',
        bus: 'bus1',
        pg: 100,
        qg: 50,
        v: 1.0,
        pmax: 200,
        pmin: 0,
        qmax: 100,
        qmin: -50,
        active: true,
        cost: {
          model: 'polynomial',
          c2: 0.001,
          c1: 20,
          c0: 100,
          startup: 1000,
          shutdown: 500,
        },
      };
      expect(gen.cost?.model).toBe('polynomial');
      expect(gen.cost?.c2).toBe(0.001);
      expect(gen.cost?.c1).toBe(20);
      expect(gen.cost?.c0).toBe(100);
    });

    it('should support piecewise cost model', () => {
      const gen: Generator = {
        id: 'gen1',
        bus: 'bus1',
        pg: 100,
        qg: 50,
        v: 1.0,
        pmax: 200,
        pmin: 0,
        qmax: 100,
        qmin: -50,
        active: true,
        cost: {
          model: 'piecewise',
          piecewise: [
            { p: 0, f: 0 },
            { p: 50, f: 1000 },
            { p: 100, f: 2200 },
          ],
        },
      };
      expect(gen.cost?.model).toBe('piecewise');
      expect(gen.cost?.piecewise).toHaveLength(3);
    });
  });

  describe('Load demand models', () => {
    it('should support all demand models', () => {
      const demandModels: Load['demandModel'][] = [
        'constant-power',
        'constant-impedance',
        'constant-current',
        'mixed',
      ];
      demandModels.forEach((dm) => {
        const load: Load = {
          id: 'load1',
          name: 'Test Load',
          bus: 'bus1',
          pl: 50,
          ql: 30,
          active: true,
          demandModel: dm,
        };
        expect(load.demandModel).toBe(dm);
      });
    });
  });

  describe('Complete Power System', () => {
    it('should create a valid power system with all components', () => {
      const system: PowerSystem = {
        name: 'Test System',
        buses: [
          {
            id: 'bus1',
            name: 'Slack Bus',
            type: 'slack',
            voltage: 1.0,
            angle: 0,
            vmin: 0.9,
            vmax: 1.1,
            area: 1,
            region: 1,
            x: 0,
            y: 0,
            active: true,
          },
          {
            id: 'bus2',
            name: 'PV Bus',
            type: 'pv',
            voltage: 1.05,
            angle: 0,
            vmin: 0.9,
            vmax: 1.1,
            area: 1,
            region: 1,
            x: 1,
            y: 0,
            active: true,
          },
          {
            id: 'bus3',
            name: 'PQ Bus',
            type: 'pq',
            voltage: 1.0,
            angle: 0,
            vmin: 0.9,
            vmax: 1.1,
            area: 1,
            region: 1,
            x: 2,
            y: 0,
            active: true,
          },
        ],
        lines: [
          {
            id: 'line1',
            fromBus: 'bus1',
            toBus: 'bus2',
            resistance: 0.02,
            reactance: 0.04,
            susceptance: 0,
            rating: 100,
            active: true,
          },
          {
            id: 'line2',
            fromBus: 'bus2',
            toBus: 'bus3',
            resistance: 0.02,
            reactance: 0.04,
            susceptance: 0,
            rating: 100,
            active: true,
          },
        ],
        transformers: [
          {
            id: 'tx1',
            fromBus: 'bus1',
            toBus: 'bus2',
            resistance: 0.01,
            reactance: 0.06,
            tap: 1.0,
            shift: 0,
            rating: 100,
            active: true,
          },
        ],
        generators: [
          {
            id: 'gen1',
            bus: 'bus1',
            pg: 100,
            qg: 50,
            v: 1.0,
            pmax: 200,
            pmin: 0,
            qmax: 100,
            qmin: -50,
            active: true,
          },
        ],
        loads: [
          {
            id: 'load1',
            bus: 'bus3',
            pl: 50,
            ql: 30,
            active: true,
          },
        ],
        shunts: [
          {
            id: 'shunt1',
            bus: 'bus2',
            g: 0,
            b: 0.02,
            active: true,
          },
        ],
        baseMVA: 100,
        baseFreq: 60,
        slackBus: 'bus1',
      };

      expect(system.name).toBe('Test System');
      expect(system.buses).toHaveLength(3);
      expect(system.lines).toHaveLength(2);
      expect(system.transformers).toHaveLength(1);
      expect(system.generators).toHaveLength(1);
      expect(system.loads).toHaveLength(1);
      expect(system.shunts).toHaveLength(1);
      expect(system.baseMVA).toBe(100);
      expect(system.baseFreq).toBe(60);
      expect(system.slackBus).toBe('bus1');
    });
  });
});
