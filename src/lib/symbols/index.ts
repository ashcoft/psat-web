/**
 * IEC/IEEE Standard Power System Symbols Library
 * Based on IEC 60617 and IEEE Std 315/315A standards
 *
 * Module structure to reduce code duplication:
 * - basic.ts: Core components (bus, generator, load, motor, line)
 * - transformers.ts: Transformer symbols
 * - protection.ts: Protection devices
 * - facts.ts: FACTS and renewable energy devices
 */

export * from './basic';
export * from './transformers';
export * from './protection';
export * from './facts';

import { IECSymbol, IECSymbolType, IECSymbolCategory } from '@/types';

// Re-export types for consumers
export type { IECSymbol, IECSymbolType, IECSymbolCategory } from '@/types';

// Symbols record
import {
  busSymbol, generatorSymbol, loadSymbol, motorSymbol, lineSymbol,
} from './basic';
import {
  transformerSymbol, transformer3WSymbol, transformerRegSymbol,
} from './transformers';
import {
  breakerSymbol, switchSymbol, disconnectSymbol, fuseSymbol, recloserSymbol,
  sectionalizerSymbol, ctSymbol, ptSymbol, relaySymbol,
} from './protection';
import {
  svcSymbol, statcomSymbol, tcscSymbol, upfcSymbol, windTurbineSymbol,
  pvArraySymbol, batterySymbol, substationSymbol, arresterSymbol,
  shuntSymbol, capacitorBankSymbol, capacitorSymbol, busbarSymbol,
  meterSymbol, groundSymbol, externalGridSymbol, equivalentSymbol,
  consortiumSymbol, junctionSymbol,
} from './facts';

export const symbols: Record<IECSymbolType, IECSymbol> = {
  bus: busSymbol,
  generator: generatorSymbol,
  load: loadSymbol,
  motor: motorSymbol,
  shunt: shuntSymbol,
  capacitor: capacitorSymbol,
  'capacitor-bank': capacitorBankSymbol,
  'reactor-bank': shuntSymbol,
  busbar: busbarSymbol,
  line: lineSymbol,
  transformer: transformerSymbol,
  'transformer-3w': transformer3WSymbol,
  'transformer-reg': transformerRegSymbol,
  breaker: breakerSymbol,
  switch: switchSymbol,
  disconnect: disconnectSymbol,
  fuse: fuseSymbol,
  sectionalizer: sectionalizerSymbol,
  recloser: recloserSymbol,
  'current-transformer': ctSymbol,
  'potential-transformer': ptSymbol,
  relay: relaySymbol,
  meter: meterSymbol,
  ground: groundSymbol,
  'external-grid': externalGridSymbol,
  equivalent: equivalentSymbol,
  svc: svcSymbol,
  statcom: statcomSymbol,
  tcsc: tcscSymbol,
  upfc: upfcSymbol,
  'wind-turbine': windTurbineSymbol,
  'pv-array': pvArraySymbol,
  battery: batterySymbol,
  substation: substationSymbol,
  consortium: consortiumSymbol,
  arrestor: arresterSymbol,
  junction: junctionSymbol,
  reactor: shuntSymbol,
};

export const symbolCategories = {
  generation: [generatorSymbol, externalGridSymbol, windTurbineSymbol],
  load: [loadSymbol, motorSymbol],
  transmission: [lineSymbol, transformerSymbol, transformer3WSymbol, transformerRegSymbol],
  distribution: [lineSymbol, breakerSymbol, switchSymbol, disconnectSymbol],
  protection: [breakerSymbol, switchSymbol, disconnectSymbol, fuseSymbol, recloserSymbol, sectionalizerSymbol, relaySymbol, arresterSymbol],
  measurement: [ctSymbol, ptSymbol, meterSymbol],
  compensation: [shuntSymbol, capacitorBankSymbol, svcSymbol, statcomSymbol, tcscSymbol, upfcSymbol],
  storage: [batterySymbol],
  renewable: [windTurbineSymbol, pvArraySymbol],
  network: [busSymbol, busbarSymbol, substationSymbol, groundSymbol, equivalentSymbol, consortiumSymbol, junctionSymbol],
  substation: [substationSymbol],
} as const;

export function getSymbol(type: IECSymbolType): IECSymbol {
  return symbols[type];
}

export function getSymbolsByCategory(category: IECSymbolCategory): IECSymbol[] {
  const categoryMap: Record<string, IECSymbol[]> = symbolCategories as unknown as Record<string, IECSymbol[]>;
  return categoryMap[category] || [];
}

export function renderSymbol(ctx: CanvasRenderingContext2D, type: IECSymbolType, x: number, y: number): void {
  const symbol = symbols[type];
  if (symbol?.render) {
    symbol.render(ctx, x, y);
  }
}
