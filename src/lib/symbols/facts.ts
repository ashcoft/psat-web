/**
 * FACTS and Renewable Energy symbols
 */

import { IECSymbol } from '@/types';

function setStroke(ctx: CanvasRenderingContext2D, color = '#000', width = 1) {
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
}

function drawFilledCircle(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

function drawCircle(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.stroke();
}

function drawLine(ctx: CanvasRenderingContext2D, x1: number, y1: number, x2: number, y2: number) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function drawRectangle(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number) {
  ctx.strokeRect(x - w / 2, y - h / 2, w, h);
}

function drawText(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, fontSize = 10) {
  ctx.font = `${fontSize}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, x, y);
}

export const svcSymbol: IECSymbol = {
  type: 'svc',
  name: 'Static VAR Compensator',
  ieeeSymbol: 'IEEE 421.5',
  category: 'transmission',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qMax', label: 'Max Reactive', type: 'number', unit: 'MVAR', default: 100 },
    { key: 'qMin', label: 'Min Reactive', type: 'number', unit: 'MVAR', default: -100 },
    { key: 'vRef', label: 'Voltage Ref', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'vdc', label: 'DC Voltage', type: 'number', unit: 'kV', default: 10 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 25;
    setStroke(ctx);
    drawLine(ctx, x + 30, y, x + 30, y + 10);
    drawRectangle(ctx, cx, cy, 35, 25);
    drawCircle(ctx, cx, cy, 10);
    drawText(ctx, 'SVC', cx, cy, 10);
    drawLine(ctx, x + 30, y + 40, x + 30, y + 50);
  },
};

export const statcomSymbol: IECSymbol = {
  type: 'statcom',
  name: 'STATCOM',
  ieeeSymbol: 'IEEE 421.5',
  category: 'transmission',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qMax', label: 'Max Reactive', type: 'number', unit: 'MVAR', default: 150 },
    { key: 'qMin', label: 'Min Reactive', type: 'number', unit: 'MVAR', default: -150 },
    { key: 'vRef', label: 'Voltage Ref', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'vdc', label: 'DC Voltage', type: 'number', unit: 'kV', default: 10 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 25;
    setStroke(ctx);
    drawLine(ctx, x + 30, y, x + 30, y + 10);
    drawRectangle(ctx, cx, cy, 40, 30);
    ctx.setLineDash([3, 3]);
    drawRectangle(ctx, cx, cy, 30, 20);
    ctx.setLineDash([]);
    drawText(ctx, 'STATCOM', cx, cy, 8);
    drawLine(ctx, x + 30, y + 40, x + 30, y + 50);
  },
};

export const tcscSymbol: IECSymbol = {
  type: 'tcsc',
  name: 'TCSC',
  ieeeSymbol: 'IEEE 421.5',
  category: 'transmission',
  width: 70,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 70, y: 20, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'xMax', label: 'Max Reactance', type: 'number', unit: 'p.u.', default: 0.2 },
    { key: 'xMin', label: 'Min Reactance', type: 'number', unit: 'p.u.', default: -0.2 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 35, cy = y + 20;
    setStroke(ctx);
    drawLine(ctx, x, y + 20, x + 15, y + 20);
    drawRectangle(ctx, cx, cy, 40, 30);
    drawLine(ctx, cx - 12, cy - 10, cx - 12, cy + 10);
    drawLine(ctx, cx, cy - 10, cx, cy + 10);
    drawLine(ctx, cx + 12, cy - 10, cx + 12, cy + 10);
    drawLine(ctx, x + 55, y + 20, x + 70, y + 20);
  },
};

export const upfcSymbol: IECSymbol = {
  type: 'upfc',
  name: 'Unified Power Flow Controller',
  ieeeSymbol: 'IEEE 421.5',
  category: 'transmission',
  width: 70,
  height: 50,
  connectionPoints: [
    { id: 'left', x: 0, y: 25, type: 'left' },
    { id: 'right', x: 70, y: 25, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pRef', label: 'P Reference', type: 'number', unit: 'MW', default: 0 },
    { key: 'qRef', label: 'Q Reference', type: 'number', unit: 'MVAR', default: 0 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 35, cy = y + 25;
    setStroke(ctx);
    drawLine(ctx, x, y + 25, x + 10, y + 25);
    drawRectangle(ctx, cx - 15, cy, 20, 35);
    drawRectangle(ctx, cx + 15, cy, 20, 35);
    drawText(ctx, 'UPFC', cx, cy, 8);
    drawLine(ctx, x + 60, y + 25, x + 70, y + 25);
  },
};

export const windTurbineSymbol: IECSymbol = {
  type: 'wind-turbine',
  name: 'Wind Turbine',
  ieeeSymbol: 'IEEE 1547',
  category: 'renewable',
  width: 60,
  height: 60,
  connectionPoints: [
    { id: 'bottom', x: 30, y: 60, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pMax', label: 'Rated Power', type: 'number', unit: 'MW', default: 2 },
    { key: 'socInitial', label: 'Initial SOC', type: 'number', unit: '%', default: 50 },
    { key: 'etaCharge', label: 'Charge Efficiency', type: 'number', default: 95 },
    { key: 'etaDischarge', label: 'Discharge Efficiency', type: 'number', default: 95 },
    { key: 'pmax', label: 'Max Power', type: 'number', unit: 'MW', default: 2 },
    { key: 'cutIn', label: 'Cut-in Wind', type: 'number', unit: 'm/s', default: 3 },
    { key: 'cutOut', label: 'Cut-out Wind', type: 'number', unit: 'm/s', default: 25 },
    { key: 'wsCutIn', label: 'Wind Speed Cut-in', type: 'number', unit: 'm/s', default: 3 },
    { key: 'wsRated', label: 'Rated Wind Speed', type: 'number', unit: 'm/s', default: 12 },
    { key: 'wsCutOut', label: 'Cut-out Wind Speed', type: 'number', unit: 'm/s', default: 25 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 15;
    setStroke(ctx);
    drawLine(ctx, x + 30, y + 20, x + 30, y + 60);
    // Turbine blades
    for (let i = 0; i < 3; i++) {
      const angle = (i * 2 * Math.PI) / 3;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(angle) * 25, cy + Math.sin(angle) * 25);
      ctx.lineWidth = 2;
      ctx.stroke();
    }
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.stroke();
  },
};

export const pvArraySymbol: IECSymbol = {
  type: 'pv-array',
  name: 'PV Array',
  ieeeSymbol: 'IEEE 1547',
  category: 'renewable',
  width: 60,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 60, y: 20, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pMax', label: 'Rated Power', type: 'number', unit: 'kW', default: 250 },
    { key: 'socInitial', label: 'Initial SOC', type: 'number', unit: '%', default: 50 },
    { key: 'etaCharge', label: 'Charge Efficiency', type: 'number', default: 95 },
    { key: 'etaDischarge', label: 'Discharge Efficiency', type: 'number', default: 95 },
    { key: 'pmax', label: 'Max Power', type: 'number', unit: 'MW', default: 2 },
    { key: 'eff', label: 'Efficiency', type: 'number', unit: '%', default: 20 },
    { key: 'area', label: 'Panel Area', type: 'number', unit: 'm²', default: 100 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 20, x + 10, y + 20);
    // Solar panel
    ctx.strokeRect(x + 10, y + 5, 40, 30);
    // Grid lines
    for (let i = 1; i < 4; i++) {
      drawLine(ctx, x + 10 + i * 10, y + 5, x + 10 + i * 10, y + 35);
    }
    for (let i = 1; i < 3; i++) {
      drawLine(ctx, x + 10, y + 5 + i * 10, x + 50, y + 5 + i * 10);
    }
    drawLine(ctx, x + 50, y + 20, x + 60, y + 20);
  },
};

export const batterySymbol: IECSymbol = {
  type: 'battery',
  name: 'Battery Storage',
  ieeeSymbol: 'IEEE 1547',
  category: 'storage',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'capacity', label: 'Capacity', type: 'number', unit: 'MWh', default: 4 },
    { key: 'socMin', label: 'Min SOC', type: 'number', unit: '%', default: 20 },
    { key: 'socMax', label: 'Max SOC', type: 'number', unit: '%', default: 90 },
    { key: 'eMax', label: 'Max Energy', type: 'number', unit: 'MWh', default: 4 },
    { key: 'eMin', label: 'Min Energy', type: 'number', unit: 'MWh', default: 0 },
    { key: 'pMax', label: 'Max Power', type: 'number', unit: 'MW', default: 2 },
    { key: 'socInitial', label: 'Initial SOC', type: 'number', unit: '%', default: 50 },
    { key: 'etaCharge', label: 'Charge Efficiency', type: 'number', default: 95 },
    { key: 'etaDischarge', label: 'Discharge Efficiency', type: 'number', default: 95 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    drawLine(ctx, x + 25, y, x + 25, y + 10);
    drawRectangle(ctx, cx, cy, 35, 25);
    drawLine(ctx, cx - 12, cy, cx + 12, cy);
    ctx.lineWidth = 3;
    drawLine(ctx, cx - 8, cy + 8, cx - 3, cy + 8);
    drawLine(ctx, cx + 3, cy + 8, cx + 8, cy + 8);
    ctx.lineWidth = 1;
    drawLine(ctx, x + 25, y + 30, x + 25, y + 40);
  },
};

export const substationSymbol: IECSymbol = {
  type: 'substation',
  name: 'Substation',
  ieeeSymbol: 'IEEE 315',
  category: 'network',
  width: 60,
  height: 60,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 60, type: 'bottom' },
    { id: 'left', x: 0, y: 30, type: 'left' },
    { id: 'right', x: 60, y: 30, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'transmission', label: 'Transmission' },
      { value: 'distribution', label: 'Distribution' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 30;
    setStroke(ctx);
    ctx.setLineDash([3, 3]);
    ctx.strokeRect(x + 5, y + 5, 50, 50);
    ctx.setLineDash([]);
    ctx.strokeRect(x + 10, y + 10, 40, 40);
    drawText(ctx, 'SS', cx, cy, 12);
  },
};

export const arresterSymbol: IECSymbol = {
  type: 'arrestor',
  name: 'Lightning Arrester',
  ieeeSymbol: 'IEEE 315 11-10-2',
  category: 'protection',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'vRating', label: 'Rating Voltage', type: 'number', unit: 'kV', default: 10 },
    { key: 'iMax', label: 'Max Discharge', type: 'number', unit: 'kA', default: 10 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 15);
    ctx.beginPath();
    ctx.moveTo(x + 20, y + 40);
    ctx.lineTo(x + 5, y + 15);
    ctx.lineTo(x + 35, y + 15);
    ctx.closePath();
    ctx.stroke();
    drawLine(ctx, x + 20, y + 40, x + 20, y + 50);
    ctx.lineWidth = 2;
    drawLine(ctx, x + 10, y + 45, x + 30, y + 45);
    drawLine(ctx, x + 12, y + 48, x + 28, y + 48);
    ctx.lineWidth = 1;
  },
};

// Additional symbols
export const shuntSymbol: IECSymbol = {
  type: 'shunt',
  name: 'Shunt Reactor',
  ieeeSymbol: 'IEEE 315',
  category: 'compensation',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'q', label: 'Reactive Power', type: 'number', unit: 'MVAR', default: 25 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 15);
    drawLine(ctx, x + 10, y + 35, x + 30, y + 35);
    drawLine(ctx, x + 10, y + 40, x + 30, y + 40);
    drawLine(ctx, x + 20, y + 40, x + 20, y + 50);
  },
};

export const capacitorBankSymbol: IECSymbol = {
  type: 'capacitor-bank',
  name: 'Capacitor Bank',
  ieeeSymbol: 'IEEE 315 11-8-1',
  category: 'compensation',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'q', label: 'Reactive Power', type: 'number', unit: 'MVAR', default: 50 },
    { key: 'v', label: 'Voltage Rating', type: 'number', unit: 'kV', default: 138 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 15);
    drawLine(ctx, x + 10, y + 25, x + 30, y + 25);
    drawLine(ctx, x + 10, y + 35, x + 30, y + 35);
    drawLine(ctx, x + 20, y + 35, x + 20, y + 50);
  },
};

export const capacitorSymbol: IECSymbol = {
  type: 'capacitor',
  name: 'Capacitor',
  ieeeSymbol: 'IEEE 315 11-8-2',
  category: 'compensation',
  width: 40,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 40, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'c', label: 'Capacitance', type: 'number', unit: 'µF', default: 100 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 12, y + 15);
    drawLine(ctx, x + 12, y + 5, x + 12, y + 25);
    drawLine(ctx, x + 18, y + 5, x + 18, y + 25);
    drawLine(ctx, x + 18, y + 15, x + 40, y + 15);
  },
};

export const busbarSymbol: IECSymbol = {
  type: 'busbar',
  name: 'Busbar',
  ieeeSymbol: 'JIC S1',
  category: 'network',
  width: 80,
  height: 10,
  connectionPoints: [
    { id: 'left', x: 0, y: 5, type: 'left' },
    { id: 'right', x: 80, y: 5, type: 'right' },
    { id: 'top', x: 40, y: 0, type: 'top' },
    { id: 'bottom', x: 40, y: 10, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'voltage', label: 'Voltage', type: 'number', unit: 'kV', default: 138 },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'A', default: 2000 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx, '#000', 3);
    drawLine(ctx, x, y + 5, x + 80, y + 5);
  },
};

export const meterSymbol: IECSymbol = {
  type: 'meter',
  name: 'Meter',
  ieeeSymbol: 'IEEE 315',
  category: 'measurement',
  width: 30,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 30, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'wattmeter', label: 'Wattmeter' },
      { value: 'varmeter', label: 'Varmeter' },
      { value: 'ammeter', label: 'Ammeter' },
      { value: 'voltmeter', label: 'Voltmeter' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawCircle(ctx, x + 15, y + 15, 12);
    drawText(ctx, 'M', x + 15, y + 15, 10);
  },
};

export const groundSymbol: IECSymbol = {
  type: 'ground',
  name: 'Ground',
  ieeeSymbol: 'IEEE 315 02-05-01',
  category: 'network',
  width: 30,
  height: 20,
  connectionPoints: [
    { id: 'top', x: 15, y: 0, type: 'top' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 15, y, x + 15, y + 8);
    ctx.lineWidth = 2;
    drawLine(ctx, x + 5, y + 8, x + 25, y + 8);
    drawLine(ctx, x + 8, y + 12, x + 22, y + 12);
    drawLine(ctx, x + 11, y + 16, x + 19, y + 16);
    ctx.lineWidth = 1;
  },
};

export const externalGridSymbol: IECSymbol = {
  type: 'external-grid',
  name: 'External Grid',
  ieeeSymbol: 'IEEE 315 11-1-1',
  category: 'generation',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'bottom', x: 25, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'v', label: 'Voltage', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'angle', label: 'Angle', type: 'number', unit: 'deg', default: 0 },
    { key: 'z', label: 'Impedance', type: 'number', unit: 'p.u.', default: 0 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    drawCircle(ctx, cx, cy, 15);
    ctx.beginPath();
    ctx.arc(cx, cy, 8, 0, Math.PI * 2);
    ctx.stroke();
    drawLine(ctx, cx - 8, cy, cx + 8, cy);
    drawLine(ctx, cx, cy - 8, cx, cy + 8);
    drawLine(ctx, cx, cy + 15, cx, cy + 20);
  },
};

export const equivalentSymbol: IECSymbol = {
  type: 'equivalent',
  name: 'Network Equivalent',
  ieeeSymbol: 'IEEE 315',
  category: 'network',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'v', label: 'Voltage', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'angle', label: 'Angle', type: 'number', unit: 'deg', default: 0 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    drawLine(ctx, x + 25, y, x + 25, y + 8);
    drawCircle(ctx, cx, cy, 12);
    drawLine(ctx, x, y + 20, x + 13, y + 20);
    drawLine(ctx, x + 37, y + 20, x + 50, y + 20);
    drawLine(ctx, x + 20, cy, cx - 12, cy);
    drawLine(ctx, cx + 12, cy, x + 30, cy);
  },
};

export const consortiumSymbol: IECSymbol = {
  type: 'consortium',
  name: 'Equivalent Impedance',
  ieeeSymbol: 'IEEE 315',
  category: 'network',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'r', label: 'Resistance', type: 'number', unit: 'p.u.', default: 0.1 },
    { key: 'x', label: 'Reactance', type: 'number', unit: 'p.u.', default: 0.2 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    drawLine(ctx, x + 15, y + 15, x + 20, y + 5);
    drawLine(ctx, x + 20, y + 5, x + 30, y + 25);
    drawLine(ctx, x + 30, y + 25, x + 40, y + 5);
    drawLine(ctx, x + 40, y + 5, x + 35, y + 15);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
  },
};

export const junctionSymbol: IECSymbol = {
  type: 'junction',
  name: 'Junction',
  ieeeSymbol: 'IEEE 315',
  category: 'network',
  width: 20,
  height: 20,
  connectionPoints: [
    { id: 'top', x: 10, y: 0, type: 'top' },
    { id: 'bottom', x: 10, y: 20, type: 'bottom' },
    { id: 'left', x: 0, y: 10, type: 'left' },
    { id: 'right', x: 20, y: 10, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawCircle(ctx, x + 10, y + 10, 5);
    drawFilledCircle(ctx, x + 10, y + 10, 3);
  },
};
