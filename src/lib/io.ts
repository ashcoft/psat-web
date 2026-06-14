import { PowerSystem, Bus, Line, Transformer, Load, Generator, Shunt, Area, Settings, defaultSettings, AnalysisConfig } from '@/types';

export function serializeSystem(system: PowerSystem): string {
  const data = {
    version: '1.0',
    generator: 'PSAT Web',
    date: new Date().toISOString(),
    system,
  };
  return JSON.stringify(data, null, 2);
}

export function deserializeSystem(json: string): PowerSystem | null {
  try {
    const data = JSON.parse(json);
    if (!data.system || !data.system.buses) return null;
    return validateSystem(data.system);
  } catch { return null; }
}

function validateSystem(system: any): PowerSystem {
  return {
    buses: (system.buses || []).map((b: any): Bus => ({
      id: String(b.id || b.name || Math.random()),
      name: String(b.name || 'Bus'),
      type: b.type === 'slack' || b.type === 'pv' || b.type === 'pq' ? b.type : 'pq',
      voltage: Number(b.voltage) || 1.0,
      angle: Number(b.angle) || 0,
      vmin: Number(b.vmin) || 0.9,
      vmax: Number(b.vmax) || 1.1,
      area: Number(b.area) || 1,
      region: Number(b.region) || 1,
      x: Number(b.x) || 0,
      y: Number(b.y) || 0,
      active: b.active !== false,
    })),
    lines: (system.lines || []).map((l: any): Line => ({
      id: String(l.id || `line_${Math.random()}`),
      fromBus: String(l.fromBus),
      toBus: String(l.toBus),
      resistance: Number(l.resistance) || 0,
      reactance: Number(l.reactance) || 0.01,
      susceptance: Number(l.susceptance) || 0,
      rating: Number(l.rating) || 100,
      active: l.active !== false,
    })),
    transformers: (system.transformers || []).map((t: any): Transformer => ({
      id: String(t.id || `txf_${Math.random()}`),
      fromBus: String(t.fromBus),
      toBus: String(t.toBus),
      tap: Number(t.tap) || 1,
      phase: Number(t.phase) || 0,
      impedance: Number(t.impedance) || 0.1,
      active: t.active !== false,
    })),
    loads: (system.loads || []).map((l: any): Load => ({
      id: String(l.id || `load_${Math.random()}`),
      busId: String(l.busId),
      pDemand: Number(l.pDemand) || 0,
      qDemand: Number(l.qDemand) || 0,
      active: l.active !== false,
    })),
    generators: (system.generators || []).map((g: any): Generator => ({
      id: String(g.id || `gen_${Math.random()}`),
      busId: String(g.busId),
      pGen: Number(g.pGen) || 0,
      qGen: Number(g.qGen) || 0,
      vSetpoint: Number(g.vSetpoint) || 1.0,
      active: g.active !== false,
    })),
    shunts: (system.shunts || []).map((s: any): Shunt => ({
      id: String(s.id || `shunt_${Math.random()}`),
      busId: String(s.busId),
      g: Number(s.g) || 0,
      b: Number(s.b) || 0,
      active: s.active !== false,
    })),
    areas: (system.areas || []).map((a: any): Area => ({
      id: String(a.id || `area_${Math.random()}`),
      name: String(a.name || 'Area'),
      slackBus: String(a.slackBus || (system.buses?.[0]?.id || '')),
    })),
  };
}

export function exportToMatpower(system: PowerSystem): string {
  const n = system.buses.length;
  const lines: string[] = [];
  lines.push('function mpc = psat_system');
  lines.push('%% PSAT Web - Converted System');
  lines.push('%%');
  lines.push(`mpc.version = '2';`);
  lines.push('mpc.baseMVA = 100;');

  lines.push('%% bus data:');
  lines.push('%% bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin');
  const busData = system.buses.map(b => {
    const type = b.type === 'slack' ? 3 : b.type === 'pv' ? 2 : 1;
    return [b.id, type, 0, 0, 0, 0, b.area, b.voltage, b.angle, 100, 1, b.vmax, b.vmin].join(' ');
  });
  lines.push(`mpc.bus = [${busData.join('; ')}];`);

  lines.push('%% generator data:');
  lines.push('%% bus Pg Qg Qmax Qmin Vg mBase status Pmax Pmin');
  const genData = system.generators.filter(g => g.active).map(g => {
    const bus = system.buses.find(b => b.id === g.busId);
    return [g.busId, g.pGen, g.qGen, 10, -10, g.vSetpoint, 100, 1, g.pGen * 2, 0].join(' ');
  });
  lines.push(`mpc.gen = [${genData.join('; ')}];`);

  lines.push('%% branch data:');
  lines.push('%% fbus tbus r x b rateA rateB rateC ratio angle status');
  const branchData = system.lines.filter(l => l.active).map(l => {
    return [l.fromBus, l.toBus, l.resistance, l.reactance, l.susceptance, l.rating, 0, 0, 1, 0, 1].join(' ');
  });
  lines.push(`mpc.branch = [${branchData.join('; ')}];`);

  return lines.join('\n');
}

export function exportToRaw(system: PowerSystem): string {
  const lines: string[] = [];
  lines.push('PSAT Web - Raw Format Export');
  lines.push(`Base MVA: 100  Frequency: 50`);
  lines.push('');

  lines.push(`BUS DATA FOLLOWS ${system.buses.length} ITEMS`);
  system.buses.forEach(b => {
    lines.push(`${b.id}, '${b.name}', ${b.voltage}, ${b.angle}, ${b.type === 'slack' ? 3 : b.type === 'pv' ? 2 : 1}, ${b.area}, ${b.vmin}, ${b.vmax}`);
  });

  lines.push('');
  lines.push(`LOAD DATA FOLLOWS ${system.loads.length} ITEMS`);
  system.loads.filter(l => l.active).forEach(l => {
    lines.push(`${l.id}, 'Load', ${l.busId}, ${l.pDemand}, ${l.qDemand}`);
  });

  lines.push('');
  lines.push(`GENERATOR DATA FOLLOWS ${system.generators.length} ITEMS`);
  system.generators.filter(g => g.active).forEach(g => {
    lines.push(`${g.id}, 'Gen', ${g.busId}, ${g.pGen}, ${g.qGen}, ${g.vSetpoint}`);
  });

  lines.push('');
  lines.push(`BRANCH DATA FOLLOWS ${system.lines.length} ITEMS`);
  system.lines.filter(l => l.active).forEach(l => {
    lines.push(`${l.id}, 'Line', ${l.fromBus}, ${l.toBus}, ${l.resistance}, ${l.reactance}, ${l.susceptance}, ${l.rating}`);
  });

  lines.push('');
  lines.push('END OF DATA');
  return lines.join('\n');
}

export function saveToFile(content: string, filename: string, type: string = 'application/json') {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function loadFromFile(): Promise<string> {
  return new Promise((resolve, reject) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json,.txt,.raw,.m';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) { reject(new Error('No file selected')); return; }
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = () => reject(reader.error);
      reader.readAsText(file);
    };
    input.click();
  });
}
