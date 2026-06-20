/**
 * Protection device symbols (breakers, switches, relays, CT/PT)
 */

import { IECSymbol } from '@/types';

function setStroke(ctx: CanvasRenderingContext2D, color = '#000', width = 1) {
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
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
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 500 },
    { key: 'iRating', label: 'Current Rating', type: 'number', unit: 'A', default: 2000 },
    { key: 'status', label: 'Status', type: 'select', options: [
      { value: 'closed', label: 'Closed' },
      { value: 'open', label: 'Open' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
    drawRectangle(ctx, x + 15, y + 15, 20, 25);
    drawLine(ctx, x + 15, y + 5, x + 35, y + 25);
  },
};

export const switchSymbol: IECSymbol = {
  type: 'switch',
  name: 'Switch',
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
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 15, x + 15, y + 15);
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
    drawCircle(ctx, x + 25, y + 15, 8);
  },
};

export const disconnectSymbol: IECSymbol = {
  type: 'disconnect',
  name: 'Disconnect Switch',
  ieeeSymbol: 'IEEE 315 11-9-3',
  category: 'protection',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 50, y: 20, type: 'right' },
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
    drawLine(ctx, x, y + 20, x + 15, y + 20);
    drawLine(ctx, x + 35, y + 20, x + 50, y + 20);
    drawLine(ctx, x + 15, y + 20, x + 35, y + 10);
    drawCircle(ctx, x + 25, y + 20, 3);
  },
};

export const fuseSymbol: IECSymbol = {
  type: 'fuse',
  name: 'Fuse',
  ieeeSymbol: 'IEEE 315 11-9-4',
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
    drawLine(ctx, x + 35, y + 15, x + 50, y + 15);
    drawRectangle(ctx, x + 25, y + 15, 10, 20);
    drawLine(ctx, x + 25, y + 5, x + 25, y + 25);
  },
};

export const recloserSymbol: IECSymbol = {
  type: 'recloser',
  name: 'Recloser',
  ieeeSymbol: 'IEEE 315 11-9-5',
  category: 'protection',
  width: 50,
  height: 35,
  connectionPoints: [
    { id: 'left', x: 0, y: 17, type: 'left' },
    { id: 'right', x: 50, y: 17, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'recloseTime', label: 'Reclose Time', type: 'number', unit: 's', default: 1 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 17, x + 12, y + 17);
    drawLine(ctx, x + 38, y + 17, x + 50, y + 17);
    drawCircle(ctx, x + 25, y + 17, 12);
    drawLine(ctx, x + 25, y + 5, x + 25, y + 29);
    drawText(ctx, 'R', x + 25, y + 17, 8);
  },
};

export const sectionalizerSymbol: IECSymbol = {
  type: 'sectionalizer',
  name: 'Sectionalizer',
  ieeeSymbol: 'IEEE 315',
  category: 'protection',
  width: 50,
  height: 35,
  connectionPoints: [
    { id: 'left', x: 0, y: 17, type: 'left' },
    { id: 'right', x: 50, y: 17, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 50 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 17, x + 12, y + 17);
    drawLine(ctx, x + 38, y + 17, x + 50, y + 17);
    drawCircle(ctx, x + 25, y + 17, 10);
    drawCircle(ctx, x + 25, y + 17, 5);
  },
};

export const ctSymbol: IECSymbol = {
  type: 'current-transformer',
  name: 'Current Transformer',
  ieeeSymbol: 'IEEE 315 15-5-1',
  category: 'measurement',
  width: 40,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'ratio', label: 'Ratio', type: 'string', default: '1000/5' },
    { key: 'class', label: 'Class', type: 'select', options: [
      { value: 'C', label: 'C (Metering)' },
      { value: 'T', label: 'T (Protection)' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 15);
    drawCircle(ctx, x + 20, y + 25, 10);
    drawLine(ctx, x + 10, y + 25, x + 30, y + 25);
    drawLine(ctx, x + 20, y + 35, x + 20, y + 40);
  },
};

export const ptSymbol: IECSymbol = {
  type: 'potential-transformer',
  name: 'Potential Transformer',
  ieeeSymbol: 'IEEE 315 15-5-2',
  category: 'measurement',
  width: 40,
  height: 45,
  connectionPoints: [
    { id: 'top', x: 20, y: 0, type: 'top' },
    { id: 'bottom', x: 20, y: 45, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'ratio', label: 'Ratio', type: 'string', default: '13800/120' },
    { key: 'class', label: 'Class', type: 'select', options: [
      { value: '0.3', label: '0.3 (Metering)' },
      { value: '1.2', label: '1.2 (Protection)' },
    ]},
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x + 20, y, x + 20, y + 10);
    ctx.beginPath();
    ctx.arc(x + 20, y + 20, 10, 0, Math.PI, true);
    ctx.stroke();
    drawLine(ctx, x + 20, y + 30, x + 20, y + 45);
    drawText(ctx, 'PT', x + 20, y + 40, 8);
  },
};

export const relaySymbol: IECSymbol = {
  type: 'relay',
  name: 'Protection Relay',
  ieeeSymbol: 'IEEE 315',
  category: 'protection',
  width: 50,
  height: 35,
  connectionPoints: [
    { id: 'left', x: 0, y: 17, type: 'left' },
    { id: 'right', x: 50, y: 17, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'type', label: 'Type', type: 'select', options: [
      { value: 'overcurrent', label: 'Overcurrent' },
      { value: 'distance', label: 'Distance' },
      { value: 'differential', label: 'Differential' },
    ]},
    { key: 'setting', label: 'Setting', type: 'number', default: 1.0 },
  ],
  render: (ctx, x, y) => {
    setStroke(ctx);
    drawLine(ctx, x, y + 17, x + 15, y + 17);
    drawLine(ctx, x + 35, y + 17, x + 50, y + 17);
    drawRectangle(ctx, x + 25, y + 17, 10, 25);
    drawCircle(ctx, x + 25, y + 17, 5);
  },
};
