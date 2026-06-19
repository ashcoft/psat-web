/**
 * IEC/IEEE Standard Power System Symbols Library
 * Based on IEC 60617 and IEEE Std 315/315A standards
 */

import { IECSymbol, IECSymbolType, IECSymbolCategory, ComponentProperty } from '@/types';

// ============================================================================
// Symbol Rendering Functions
// ============================================================================

function setStroke(ctx: CanvasRenderingContext2D, color = '#000', width = 1) {
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
}

function setFill(ctx: CanvasRenderingContext2D, color = '#000') {
  ctx.fillStyle = color;
}

function drawCircle(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.stroke();
}

function drawFilledCircle(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
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

function drawFilledRectangle(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number) {
  ctx.fillRect(x - w / 2, y - h / 2, w, h);
}

function drawText(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, fontSize = 10) {
  ctx.font = `${fontSize}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, x, y);
}

// ============================================================================
// Individual Symbol Definitions
// ============================================================================

export const busSymbol: IECSymbol = {
  type: 'bus',
  name: 'Bus',
  ieeeSymbol: 'JIC S1',
  category: 'network',
  width: 30,
  height: 10,
  connectionPoints: [
    { id: 'top', x: 15, y: 0, type: 'top' },
    { id: 'bottom', x: 15, y: 10, type: 'bottom' },
    { id: 'left', x: 0, y: 5, type: 'left' },
    { id: 'right', x: 30, y: 5, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'voltage', label: 'Voltage (kV)', type: 'number', unit: 'kV', default: 138 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x - 15, y, x + 15, y);
  },
};

export const generatorSymbol: IECSymbol = {
  type: 'generator',
  name: 'Synchronous Generator',
  ieeeSymbol: 'IEEE 315 11-2-1',
  category: 'generation',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pg', label: 'P Generation', type: 'number', unit: 'MW', default: 100 },
    { key: 'qg', label: 'Q Generation', type: 'number', unit: 'MVAR', default: 50 },
    { key: 'v', label: 'Voltage Setpoint', type: 'number', unit: 'p.u.', default: 1.0, min: 0.9, max: 1.1 },
    { key: 'pmax', label: 'P Max', type: 'number', unit: 'MW', default: 200 },
    { key: 'pmin', label: 'P Min', type: 'number', unit: 'MW', default: 0 },
    { key: 'qmax', label: 'Q Max', type: 'number', unit: 'MVAR', default: 100 },
    { key: 'qmin', label: 'Q Min', type: 'number', unit: 'MVAR', default: -50 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    // Circle
    drawCircle(ctx, cx, cy, 15);
    // Inner circle
    ctx.beginPath();
    ctx.arc(cx, cy, 8, 0, Math.PI * 2);
    ctx.stroke();
    // Lines from center
    drawLine(ctx, cx, cy - 8, cx, cy - 15);
    drawLine(ctx, cx - 8, cy, cx + 8, cy);
    drawLine(ctx, cx, cy + 8, cx, cy + 15);
  },
};

export const loadSymbol: IECSymbol = {
  type: 'load',
  name: 'Load',
  ieeeSymbol: 'IEEE 315 10-3-1',
  category: 'load',
  width: 40,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pl', label: 'P Demand', type: 'number', unit: 'MW', default: 50 },
    { key: 'ql', label: 'Q Demand', type: 'number', unit: 'MVAR', default: 30 },
    { key: 'demandModel', label: 'Demand Model', type: 'select', options: [
      { value: 'constant-power', label: 'Constant Power' },
      { value: 'constant-impedance', label: 'Constant Impedance' },
      { value: 'constant-current', label: 'Constant Current' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 20, cy = y + 20;
    setStroke(ctx);
    // Rectangle
    drawRectangle(ctx, cx, cy, 25, 25);
    // Diagonal lines inside
    drawLine(ctx, cx - 10, cy - 10, cx + 10, cy + 10);
    drawLine(ctx, cx - 10, cy + 10, cx + 10, cy - 10);
  },
};

export const motorSymbol: IECSymbol = {
  type: 'motor',
  name: 'Motor',
  ieeeSymbol: 'IEEE 315 11-4-1',
  category: 'load',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pm', label: 'Motor Power', type: 'number', unit: 'MW', default: 50 },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'induction', label: 'Induction' },
      { value: 'synchronous', label: 'Synchronous' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    // Circle with M
    drawCircle(ctx, cx, cy, 15);
    drawText(ctx, 'M', cx, cy, 14);
  },
};

export const lineSymbol: IECSymbol = {
  type: 'line',
  name: 'Transmission Line',
  ieeeSymbol: 'IEEE 315 11-5-1',
  category: 'transmission',
  width: 60,
  height: 20,
  connectionPoints: [
    { id: 'left', x: 0, y: 10, type: 'left' },
    { id: 'right', x: 60, y: 10, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'r', label: 'Resistance', type: 'number', unit: 'p.u.', default: 0.01 },
    { key: 'x', label: 'Reactance', type: 'number', unit: 'p.u.', default: 0.04 },
    { key: 'b', label: 'Susceptance', type: 'number', unit: 'p.u.', default: 0 },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'length', label: 'Length', type: 'number', unit: 'km', default: 100 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 10, x + 60, y + 10);
    // Add impedance box in middle
    drawRectangle(ctx, x + 30, y + 10, 15, 10);
  },
};

export const transformerSymbol: IECSymbol = {
  type: 'transformer',
  name: 'Two-Winding Transformer',
  ieeeSymbol: 'IEEE 315 11-6-1',
  category: 'transmission',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'r', label: 'Resistance', type: 'number', unit: 'p.u.', default: 0.01 },
    { key: 'x', label: 'Reactance', type: 'number', unit: 'p.u.', default: 0.06 },
    { key: 'tap', label: 'Tap Ratio', type: 'number', unit: 'p.u.', default: 1.0, min: 0.8, max: 1.2 },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'vectorGroup', label: 'Vector Group', type: 'select', options: [
      { value: 'Yy0', label: 'Yy0' },
      { value: 'Yy6', label: 'Yy6' },
      { value: 'Dy11', label: 'Dy11' },
      { value: 'Dy5', label: 'Dy5' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 25;
    setStroke(ctx);
    // H-bird shape
    drawLine(ctx, x + 30, y, x + 30, y + 10);
    drawLine(ctx, x + 30, y + 40, x + 30, y + 50);
    // Horizontal bars
    drawLine(ctx, x + 15, y + 10, x + 45, y + 10);
    drawLine(ctx, x + 15, y + 40, x + 45, y + 40);
    // Vertical bar
    drawLine(ctx, x + 30, y + 10, x + 30, y + 40);
  },
};

export const transformer3WSymbol: IECSymbol = {
  type: 'transformer-3w',
  name: 'Three-Winding Transformer',
  ieeeSymbol: 'IEEE 315 11-6-2',
  category: 'transmission',
  width: 70,
  height: 60,
  connectionPoints: [
    { id: 'top', x: 35, y: 0, type: 'top' },
    { id: 'left', x: 0, y: 30, type: 'left' },
    { id: 'right', x: 70, y: 30, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating1', label: 'Winding 1 Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'rating2', label: 'Winding 2 Rating', type: 'number', unit: 'MVA', default: 50 },
    { key: 'rating3', label: 'Winding 3 Rating', type: 'number', unit: 'MVA', default: 30 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    // Three lines
    drawLine(ctx, x + 35, y, x + 35, y + 20);
    drawLine(ctx, x, y + 30, x + 20, y + 30);
    drawLine(ctx, x + 50, y + 30, x + 70, y + 30);
    // Common point
    drawCircle(ctx, x + 35, y + 30, 5);
    // Three impedance boxes
    drawRectangle(ctx, x + 35, y + 12, 12, 8);
    drawRectangle(ctx, x + 10, y + 30, 8, 12);
    drawRectangle(ctx, x + 60, y + 30, 8, 12);
  },
};

export const transformerRegSymbol: IECSymbol = {
  type: 'transformer-reg',
  name: 'Regulating Transformer',
  ieeeSymbol: 'IEEE 315 11-6-3',
  category: 'transmission',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'r', label: 'Resistance', type: 'number', unit: 'p.u.', default: 0.01 },
    { key: 'x', label: 'Reactance', type: 'number', unit: 'p.u.', default: 0.06 },
    { key: 'tapMin', label: 'Min Tap', type: 'number', unit: 'p.u.', default: 0.9 },
    { key: 'tapMax', label: 'Max Tap', type: 'number', unit: 'p.u.', default: 1.1 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    // Same as regular transformer but with arrow
    drawLine(ctx, x + 30, y, x + 30, y + 10);
    drawLine(ctx, x + 30, y + 40, x + 30, y + 50);
    drawLine(ctx, x + 15, y + 10, x + 45, y + 10);
    drawLine(ctx, x + 15, y + 40, x + 45, y + 40);
    drawLine(ctx, x + 30, y + 10, x + 30, y + 40);
    // Arrow indicating regulation
    ctx.beginPath();
    ctx.moveTo(x + 50, y + 25);
    ctx.lineTo(x + 55, y + 20);
    ctx.lineTo(x + 55, y + 30);
    ctx.closePath();
    ctx.fill();
  },
};

export const shuntSymbol: IECSymbol = {
  type: 'shunt',
  name: 'Shunt Reactor/Capacitor',
  ieeeSymbol: 'IEEE 315 10-8-1',
  category: 'compensation',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'g', label: 'Conductance', type: 'number', unit: 'p.u.', default: 0 },
    { key: 'b', label: 'Susceptance', type: 'number', unit: 'p.u.', default: 0.02 },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'capacitor', label: 'Capacitor (positive B)' },
      { value: 'reactor', label: 'Reactor (negative B)' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 20;
    setStroke(ctx);
    // Line from top
    drawLine(ctx, cx, y, cx, y + 15);
    // Capacitor plates (two lines with gap)
    drawLine(ctx, cx - 10, y + 15, cx - 10, y + 35);
    drawLine(ctx, cx + 10, y + 15, cx + 10, y + 35);
    // Line to bottom
    drawLine(ctx, cx, y + 35, cx, y + 50);
    // Ground line
    ctx.lineWidth = 2;
    drawLine(ctx, cx - 10, y + 45, cx + 10, y + 45);
  },
};

export const capacitorBankSymbol: IECSymbol = {
  type: 'capacitor-bank',
  name: 'Capacitor Bank',
  ieeeSymbol: 'IEEE 315 10-8-2',
  category: 'compensation',
  width: 50,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qc', label: 'Reactive Power', type: 'number', unit: 'MVAR', default: 25 },
    { key: 'steps', label: 'Number of Steps', type: 'number', default: 4 },
    { key: 'vlow', label: 'Low Voltage Limit', type: 'number', unit: 'p.u.', default: 0.95 },
    { key: 'vhigh', label: 'High Voltage Limit', type: 'number', unit: 'p.u.', default: 1.05 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25;
    setStroke(ctx);
    drawLine(ctx, cx, y, cx, y + 12);
    // Multiple capacitor symbols
    for (let i = 0; i < 3; i++) {
      const offsetX = (i - 1) * 12;
      drawLine(ctx, cx + offsetX, y + 12, cx + offsetX, y + 22);
      drawLine(ctx, cx + offsetX - 6, y + 12, cx + offsetX + 6, y + 12);
      drawLine(ctx, cx + offsetX - 6, y + 22, cx + offsetX + 6, y + 22);
      drawLine(ctx, cx + offsetX, y + 22, cx + offsetX, y + 32);
    }
    drawLine(ctx, cx, y + 32, cx, y + 50);
  },
};

export const capacitorSymbol: IECSymbol = {
  type: 'capacitor',
  name: 'Capacitor',
  ieeeSymbol: 'IEEE 315 10-8-1',
  category: 'compensation',
  width: 40,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'c', label: 'Capacitance', type: 'number', unit: 'µF', default: 100 },
    { key: 'v', label: 'Voltage Rating', type: 'number', unit: 'kV', default: 10 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 20;
    setStroke(ctx);
    drawLine(ctx, cx, y, cx, y + 15);
    // Single capacitor symbol (two plates)
    drawLine(ctx, cx - 8, y + 15, cx + 8, y + 15);
    drawLine(ctx, cx - 8, y + 25, cx + 8, y + 25);
    drawLine(ctx, cx, y + 25, cx, y + 40);
  },
};

export const breakerSymbol: IECSymbol = {
  type: 'breaker',
  name: 'Circuit Breaker',
  ieeeSymbol: 'IEEE 315 11-9-1',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
    { key: 'rating', label: 'Rating', type: 'number', unit: 'A', default: 1000 },
    { key: 'interruptingRating', label: 'Interrupting Rating', type: 'number', unit: 'kA', default: 25 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Breaker symbol (diagonal line at 45 degrees)
    drawLine(ctx, x + 15, y + 15, x + 35, y + 5);
    drawLine(ctx, x + 35, y + 25, x + 50, y + 15);
  },
};

export const switchSymbol: IECSymbol = {
  type: 'switch',
  name: 'Switch',
  ieeeSymbol: 'IEEE 315 11-9-5',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 20, y + 15);
    drawLine(ctx, x + 20, y + 15, x + 40, y + 5);
    drawLine(ctx, x + 40, y + 25, x + 50, y + 15);
  },
};

export const disconnectSymbol: IECSymbol = {
  type: 'disconnect',
  name: 'Disconnect Switch',
  ieeeSymbol: 'IEEE 315 11-9-6',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Circle for disconnect
    drawCircle(ctx, x + 25, y + 15, 6);
    drawLine(ctx, x + 31, y + 15, x + 50, y + 15);
  },
};

export const fuseSymbol: IECSymbol = {
  type: 'fuse',
  name: 'Fuse',
  ieeeSymbol: 'IEEE 315 11-9-7',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'A', default: 100 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Rectangle with diagonal line through it
    drawRectangle(ctx, x + 25, y + 15, 15, 20);
    drawLine(ctx, x + 17, y + 5, x + 32, y + 25);
    drawLine(ctx, x + 33, y + 5, x + 18, y + 25);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
  },
};

export const recloserSymbol: IECSymbol = {
  type: 'recloser',
  name: 'Recloser',
  ieeeSymbol: 'IEEE 315 11-9-2',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
    { key: 'rating', label: 'Rating', type: 'number', unit: 'A', default: 630 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Circle with recloser symbol
    drawCircle(ctx, x + 25, y + 15, 8);
    // X inside circle
    drawLine(ctx, x + 20, y + 10, x + 30, y + 20);
    drawLine(ctx, x + 20, y + 20, x + 30, y + 10);
    drawLine(ctx, x + 33, y + 15, x + 50, y + 15);
  },
};

export const sectionalizerSymbol: IECSymbol = {
  type: 'sectionalizer',
  name: 'Sectionalizer',
  ieeeSymbol: 'IEEE 315 11-9-8',
  category: 'protection',
  width: 50,
  height: 30,
  connectionPoints: [
    { id: 'left', x: 0, y: 15, type: 'left' },
    { id: 'right', x: 50, y: 15, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Rectangle with two sections
    drawRectangle(ctx, x + 25, y + 15, 20, 20);
    drawLine(ctx, x + 25, y + 15, x + 35, y + 5);
    drawLine(ctx, x + 35, y + 25, x + 45, y + 15);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
  },
};

export const ctSymbol: IECSymbol = {
  type: 'current-transformer',
  name: 'Current Transformer',
  ieeeSymbol: 'IEEE 315 15-3-1',
  category: 'measurement',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 50, y: 20, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'ratio', label: 'Ratio', type: 'string', default: '1000/5' },
    { key: 'accuracy', label: 'Accuracy Class', type: 'string', default: '0.3' },
    { key: 'burden', label: 'Burden', type: 'number', unit: 'VA', default: 15 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 20, x + 15, y + 20);
    // CT circle with primary through
    drawCircle(ctx, x + 28, y + 20, 10);
    // Primary line through center
    drawLine(ctx, x + 28, y + 5, x + 28, y + 35);
    // Secondary dots
    ctx.fillStyle = '#000';
    drawFilledCircle(ctx, x + 25, y + 17, 2);
    drawFilledCircle(ctx, x + 31, y + 23, 2);
    drawLine(ctx, x + 38, y + 20, x + 50, y + 20);
  },
};

export const ptSymbol: IECSymbol = {
  type: 'potential-transformer',
  name: 'Potential Transformer',
  ieeeSymbol: 'IEEE 315 15-3-2',
  category: 'measurement',
  width: 50,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'ratio', label: 'Ratio', type: 'string', default: '13800/120' },
    { key: 'accuracy', label: 'Accuracy Class', type: 'string', default: '0.3' },
    { key: 'burden', label: 'Burden', type: 'number', unit: 'VA', default: 50 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25;
    setStroke(ctx);
    drawLine(ctx, cx, y, cx, y + 15);
    // PT with polarity mark
    drawCircle(ctx, cx, y + 25, 12);
    ctx.fillStyle = '#000';
    drawFilledCircle(ctx, cx - 3, y + 22, 2);
    drawLine(ctx, cx, y + 37, cx, y + 50);
  },
};

export const relaySymbol: IECSymbol = {
  type: 'relay',
  name: 'Protection Relay',
  ieeeSymbol: 'IEEE 315 15-5-1',
  category: 'protection',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'left', x: 0, y: 25, type: 'left' },
    { id: 'right', x: 40, y: 25, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'type', label: 'Relay Type', type: 'select', options: [
      { value: 'overcurrent', label: 'Overcurrent' },
      { value: 'distance', label: 'Distance' },
      { value: 'differential', label: 'Differential' },
      { value: 'overvoltage', label: 'Overvoltage' },
      { value: 'undervoltage', label: 'Undervoltage' },
    ]},
    { key: 'pickup', label: 'Pickup Setting', type: 'number', default: 1.0 },
    { key: 'timeDial', label: 'Time Dial', type: 'number', default: 1.0 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 25, x + 10, y + 25);
    // Square with circle
    drawRectangle(ctx, x + 20, y + 25, 15, 25);
    drawCircle(ctx, x + 20, y + 30, 5);
    drawLine(ctx, x + 35, y + 25, x + 40, y + 25);
  },
};

export const groundSymbol: IECSymbol = {
  type: 'ground',
  name: 'Ground',
  ieeeSymbol: 'IEEE 315 02-15-1',
  category: 'network',
  width: 30,
  height: 25,
  connectionPoints: [
    { id: 'top', x: 15, y: 0, type: 'top' },
  ],
  properties: [
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'solid', label: 'Solid Ground' },
      { value: 'impedance', label: 'Impedance Ground' },
      { value: 'isolated', label: 'Isolated Ground' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 15, y, x + 15, y + 10);
    // Horizontal lines
    ctx.lineWidth = 2;
    drawLine(ctx, x + 5, y + 10, x + 25, y + 10);
    drawLine(ctx, x + 8, y + 15, x + 22, y + 15);
    drawLine(ctx, x + 11, y + 20, x + 19, y + 20);
  },
};

export const externalGridSymbol: IECSymbol = {
  type: 'external-grid',
  name: 'External Grid/Infinite Bus',
  ieeeSymbol: 'IEEE 315 11-2-2',
  category: 'generation',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'v', label: 'Voltage', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'angle', label: 'Angle', type: 'number', unit: 'deg', default: 0 },
    { key: 'scMvA', label: 'Short Circuit MVA', type: 'number', unit: 'MVA', default: 10000 },
    { key: 'zxRatio', label: 'ZX Ratio', type: 'number', default: 0.1 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25;
    setStroke(ctx);
    drawLine(ctx, cx, y, cx, y + 10);
    // Circle with internal thick line
    drawCircle(ctx, cx, y + 22, 12);
    ctx.lineWidth = 3;
    drawLine(ctx, cx - 12, y + 22, cx + 12, y + 22);
    ctx.lineWidth = 1;
  },
};

export const svcSymbol: IECSymbol = {
  type: 'svc',
  name: 'Static VAR Compensator',
  ieeeSymbol: 'IEEE 1159.1',
  category: 'compensation',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qMax', label: 'Max Reactive Power', type: 'number', unit: 'MVAR', default: 100 },
    { key: 'qMin', label: 'Min Reactive Power', type: 'number', unit: 'MVAR', default: -100 },
    { key: 'vRef', label: 'Voltage Reference', type: 'number', unit: 'p.u.', default: 1.0 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 30, y, x + 30, y + 12);
    // SVC box
    drawRectangle(ctx, x + 30, y + 25, 40, 25);
    // SVC text
    drawText(ctx, 'SVC', x + 30, y + 25, 10);
    drawLine(ctx, x + 30, y + 38, x + 30, y + 50);
  },
};

export const statcomSymbol: IECSymbol = {
  type: 'statcom',
  name: 'STATCOM',
  ieeeSymbol: 'IEEE 1159.1',
  category: 'compensation',
  width: 60,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'bottom', x: 30, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qMax', label: 'Max Reactive Power', type: 'number', unit: 'MVAR', default: 100 },
    { key: 'qMin', label: 'Min Reactive Power', type: 'number', unit: 'MVAR', default: -100 },
    { key: 'vRef', label: 'Voltage Reference', type: 'number', unit: 'p.u.', default: 1.0 },
    { key: 'vdc', label: 'DC Voltage', type: 'number', unit: 'kV', default: 10 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 30, y, x + 30, y + 12);
    // STATCOM with H-bridge symbol
    drawRectangle(ctx, x + 30, y + 25, 40, 25);
    // H-bridge inside
    drawLine(ctx, x + 15, y + 32, x + 45, y + 32);
    drawLine(ctx, x + 15, y + 43, x + 45, y + 43);
    drawLine(ctx, x + 20, y + 32, x + 20, y + 43);
    drawLine(ctx, x + 40, y + 32, x + 40, y + 43);
    drawText(ctx, 'STATCOM', x + 30, y + 12, 6);
    drawLine(ctx, x + 30, y + 38, x + 30, y + 50);
  },
};

export const tcscSymbol: IECSymbol = {
  type: 'tcsc',
  name: 'Thyristor Controlled Series Capacitor',
  ieeeSymbol: 'IEEE 1159.1',
  category: 'compensation',
  width: 60,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 60, y: 20, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'xL', label: 'Inductive Reactance', type: 'number', unit: 'p.u.', default: 0.1 },
    { key: 'xC', label: 'Capacitive Reactance', type: 'number', unit: 'p.u.', default: 0.3 },
    { key: 'alphaMin', label: 'Min Firing Angle', type: 'number', unit: 'deg', default: 145 },
    { key: 'alphaMax', label: 'Max Firing Angle', type: 'number', unit: 'deg', default: 180 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 20, x + 15, y + 20);
    // TCSC box
    drawRectangle(ctx, x + 30, y + 20, 30, 30);
    // Thyristor symbol inside
    drawLine(ctx, x + 35, y + 12, x + 35, y + 28);
    drawLine(ctx, x + 25, y + 20, x + 30, y + 15);
    drawLine(ctx, x + 25, y + 20, x + 30, y + 25);
    // Capacitor
    drawLine(ctx, x + 50, y + 12, x + 50, y + 28);
    drawLine(ctx, x + 45, y + 12, x + 55, y + 12);
    drawLine(ctx, x + 45, y + 28, x + 55, y + 28);
    drawLine(ctx, x + 45, y + 20, x + 50, y + 20);
    drawLine(ctx, x + 55, y + 20, x + 60, y + 20);
  },
};

export const upfcSymbol: IECSymbol = {
  type: 'upfc',
  name: 'Unified Power Flow Controller',
  ieeeSymbol: 'IEEE 1159.1',
  category: 'compensation',
  width: 70,
  height: 50,
  connectionPoints: [
    { id: 'left', x: 0, y: 25, type: 'left' },
    { id: 'right', x: 70, y: 25, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'qMax', label: 'Max Reactive Power', type: 'number', unit: 'MVAR', default: 100 },
    { key: 'pMax', label: 'Max Active Power', type: 'number', unit: 'MW', default: 100 },
    { key: 'vdc', label: 'DC Voltage', type: 'number', unit: 'kV', default: 10 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 25, x + 15, y + 25);
    // UPFC box
    drawRectangle(ctx, x + 35, y + 25, 40, 35);
    drawText(ctx, 'UPFC', x + 35, y + 18, 8);
    // Converter symbols inside
    drawLine(ctx, x + 25, y + 12, x + 45, y + 12);
    drawLine(ctx, x + 25, y + 38, x + 45, y + 38);
    drawLine(ctx, x + 55, y + 25, x + 70, y + 25);
  },
};

export const windTurbineSymbol: IECSymbol = {
  type: 'wind-turbine',
  name: 'Wind Turbine',
  ieeeSymbol: 'IEC 61850-7-4',
  category: 'renewable',
  width: 50,
  height: 60,
  connectionPoints: [
    { id: 'bottom', x: 25, y: 60, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pmax', label: 'Max Power', type: 'number', unit: 'MW', default: 50 },
    { key: 'wsCutIn', label: 'Cut-in Wind Speed', type: 'number', unit: 'm/s', default: 3 },
    { key: 'wsRated', label: 'Rated Wind Speed', type: 'number', unit: 'm/s', default: 12 },
    { key: 'wsCutOut', label: 'Cut-out Wind Speed', type: 'number', unit: 'm/s', default: 25 },
    { key: 'type', label: 'Generator Type', type: 'select', options: [
      { value: 'TypeA', label: 'Type A (SCIG)' },
      { value: 'TypeB', label: 'Type B (WRIG)' },
      { value: 'TypeC', label: 'Type C (DFIG)' },
      { value: 'TypeD', label: 'Type D (PMSG)' },
    ]},
  ],
  render: (ctx, x, y) => {
    const cx = x + 25;
    setStroke(ctx);
    // Tower
    drawLine(ctx, cx, y + 20, cx, y + 60);
    // Rotor hub
    drawCircle(ctx, cx, y + 20, 4);
    // Blades
    for (let i = 0; i < 3; i++) {
      const angle = (i * 120 - 90) * Math.PI / 180;
      drawLine(ctx, cx, y + 20, cx + 18 * Math.cos(angle), y + 20 + 18 * Math.sin(angle));
    }
  },
};

export const pvArraySymbol: IECSymbol = {
  type: 'pv-array',
  name: 'PV Solar Array',
  ieeeSymbol: 'IEC 61850-7-4',
  category: 'renewable',
  width: 50,
  height: 50,
  connectionPoints: [
    { id: 'bottom', x: 25, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'pmax', label: 'Max Power', type: 'number', unit: 'MW', default: 50 },
    { key: 'vMax', label: 'Max Voltage', type: 'number', unit: 'p.u.', default: 1.1 },
    { key: 'vMin', label: 'Min Voltage', type: 'number', unit: 'p.u.', default: 0.9 },
    { key: 'pfMin', label: 'Min Power Factor', type: 'number', default: 0.85 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    // Panel outline
    drawRectangle(ctx, x + 25, y + 20, 40, 30);
    // Grid lines
    drawLine(ctx, x + 25, y + 27, x + 65, y + 27);
    drawLine(ctx, x + 25, y + 33, x + 65, y + 33);
    drawLine(ctx, x + 38, y + 5, x + 38, y + 35);
    drawLine(ctx, x + 52, y + 5, x + 52, y + 35);
    // Connection
    drawLine(ctx, x + 25, y + 35, x + 25, y + 50);
  },
};

export const batterySymbol: IECSymbol = {
  type: 'battery',
  name: 'Battery Energy Storage',
  ieeeSymbol: 'IEEE 2800',
  category: 'storage',
  width: 50,
  height: 50,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 50, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'eMax', label: 'Max Energy', type: 'number', unit: 'MWh', default: 100 },
    { key: 'pMax', label: 'Max Power', type: 'number', unit: 'MW', default: 50 },
    { key: 'eMin', label: 'Min Energy', type: 'number', unit: 'MWh', default: 20 },
    { key: 'socInitial', label: 'Initial SOC', type: 'number', unit: '%', default: 50 },
    { key: 'etaCharge', label: 'Charge Efficiency', type: 'number', default: 0.95 },
    { key: 'etaDischarge', label: 'Discharge Efficiency', type: 'number', default: 0.95 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 25, y, x + 25, y + 10);
    // Battery symbol
    drawRectangle(ctx, x + 25, y + 25, 30, 20);
    // Plus and minus
    drawText(ctx, '+', x + 15, y + 25, 10);
    drawText(ctx, '-', x + 35, y + 25, 14);
    drawLine(ctx, x + 25, y + 35, x + 25, y + 50);
  },
};

export const busbarSymbol: IECSymbol = {
  type: 'busbar',
  name: 'Busbar',
  ieeeSymbol: 'IEEE 315',
  category: 'substation',
  width: 80,
  height: 10,
  connectionPoints: [
    { id: 'left', x: 0, y: 5, type: 'left' },
    { id: 'right', x: 80, y: 5, type: 'right' },
    { id: 'top1', x: 20, y: 0, type: 'top' },
    { id: 'top2', x: 40, y: 0, type: 'top' },
    { id: 'top3', x: 60, y: 0, type: 'top' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'voltage', label: 'Voltage', type: 'number', unit: 'kV', default: 138 },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'A', default: 2000 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    ctx.lineWidth = 3;
    drawLine(ctx, x, y + 5, x + 80, y + 5);
  },
};

export const substationSymbol: IECSymbol = {
  type: 'substation',
  name: 'Substation',
  ieeeSymbol: 'IEEE 315',
  category: 'substation',
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
    { key: 'vHigh', label: 'High Voltage', type: 'number', unit: 'kV', default: 230 },
    { key: 'vLow', label: 'Low Voltage', type: 'number', unit: 'kV', default: 69 },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'transmission', label: 'Transmission' },
      { value: 'distribution', label: 'Distribution' },
      { value: 'switching', label: 'Switching' },
      { value: 'collector', label: 'Wind Farm Collector' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    // Square substation boundary
    drawRectangle(ctx, x + 30, y + 30, 45, 45);
    // Substation symbol
    ctx.setLineDash([3, 3]);
    drawRectangle(ctx, x + 30, y + 30, 45, 45);
    ctx.setLineDash([]);
    drawText(ctx, 'SS', x + 30, y + 30, 12);
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
    { key: 'iMax', label: 'Max Discharge Current', type: 'number', unit: 'kA', default: 10 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 15);
    // Triangle pointing down
    ctx.beginPath();
    ctx.moveTo(x + 20, y + 40);
    ctx.lineTo(x + 5, y + 15);
    ctx.lineTo(x + 35, y + 15);
    ctx.closePath();
    ctx.stroke();
    drawLine(ctx, x + 20, y + 40, x + 20, y + 50);
    // Ground
    ctx.lineWidth = 2;
    drawLine(ctx, x + 10, y + 45, x + 30, y + 45);
    drawLine(ctx, x + 12, y + 48, x + 28, y + 48);
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
    { key: 'v', label: 'Voltage', type: 'number', unit: 'p.u.', default: 1.0 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    // Zigzag impedance
    drawLine(ctx, x + 15, y + 15, x + 20, y + 5);
    drawLine(ctx, x + 20, y + 5, x + 30, y + 25);
    drawLine(ctx, x + 30, y + 25, x + 40, y + 5);
    drawLine(ctx, x + 40, y + 5, x + 35, y + 15);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
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
    { key: 'scMvA', label: 'Short Circuit MVA', type: 'number', unit: 'MVA', default: 1000 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 25, y, x + 25, y + 10);
    // Circle with Z
    drawCircle(ctx, x + 25, y + 22, 12);
    drawText(ctx, 'Z', x + 25, y + 22, 12);
  },
};

export const meterSymbol: IECSymbol = {
  type: 'meter',
  name: 'Meter',
  ieeeSymbol: 'IEEE 315',
  category: 'measurement',
  width: 40,
  height: 50,
  connectionPoints: [
    { id: 'left', x: 0, y: 25, type: 'left' },
    { id: 'right', x: 40, y: 25, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'type', label: 'Meter Type', type: 'select', options: [
      { value: 'w', label: 'Wattmeter' },
      { value: 'v', label: 'Voltmeter' },
      { value: 'a', label: 'Ammeter' },
      { value: 'var', label: 'Varmeter' },
      { value: 'pf', label: 'Power Factor Meter' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 25, x + 10, y + 25);
    // Circle meter
    drawCircle(ctx, x + 25, y + 25, 12);
    // Pointer
    ctx.beginPath();
    ctx.moveTo(x + 25, y + 25);
    ctx.lineTo(x + 32, y + 18);
    ctx.stroke();
    drawText(ctx, 'M', x + 25, y + 38, 8);
    drawLine(ctx, x + 35, y + 25, x + 40, y + 25);
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
    setFill(ctx, '#000');
    drawFilledCircle(ctx, x + 10, y + 10, 5);
  },
};

// ============================================================================
// Symbol Registry
// ============================================================================

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
  transmission: [lineSymbol, transformerSymbol, 'transformer-3w', 'transformer-reg'].map(t => symbols[t as IECSymbolType]),
  distribution: [lineSymbol, breakerSymbol, switchSymbol, disconnectSymbol],
  protection: [breakerSymbol, switchSymbol, disconnectSymbol, fuseSymbol, recloserSymbol, sectionalizerSymbol, relaySymbol, arresterSymbol],
  measurement: [ctSymbol, ptSymbol, meterSymbol],
  compensation: [shuntSymbol, capacitorBankSymbol, svcSymbol, statcomSymbol, tcscSymbol, upfcSymbol],
  storage: [batterySymbol],
  renewable: [windTurbineSymbol, pvArraySymbol],
  substation: [substationSymbol, busbarSymbol],
  network: [busSymbol, groundSymbol, equivalentSymbol, consortiumSymbol, junctionSymbol],
};

export function getSymbol(type: IECSymbolType): IECSymbol {
  return symbols[type] || busSymbol;
}

export function getSymbolsByCategory(category: IECSymbolCategory): IECSymbol[] {
  return symbolCategories[category] || [];
}

export function renderSymbol(
  ctx: CanvasRenderingContext2D,
  type: IECSymbolType,
  x: number,
  y: number,
  rotation = 0
) {
  const symbol = getSymbol(type);
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation * Math.PI / 180);
  symbol.render(ctx, -symbol.width / 2, -symbol.height / 2);
  ctx.restore();
}
