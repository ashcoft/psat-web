/**
 * Transformer symbols (2-winding, 3-winding, regulators)
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

function drawFilledCircle(ctx: CanvasRenderingContext2D, x: number, y: number, r: number) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

export const transformerSymbol: IECSymbol = {
  type: 'transformer',
  name: 'Two-Winding Transformer',
  ieeeSymbol: 'IEEE 315 11-6-1',
  category: 'transmission',
  width: 50,
  height: 40,
  connectionPoints: [
    { id: 'top', x: 25, y: 0, type: 'top' },
    { id: 'bottom', x: 25, y: 40, type: 'bottom' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'tap', label: 'Tap Position', type: 'number', default: 0 },
    { key: 'vectorGroup', label: 'Vector Group', type: 'string', default: 'Dyn11' },
    { key: 'vHigh', label: 'HV Voltage', type: 'number', unit: 'kV', default: 230 },
    { key: 'vLow', label: 'LV Voltage', type: 'number', unit: 'kV', default: 138 },
    { key: 'x', label: 'Reactance', type: 'number', unit: 'p.u.', default: 0.1 },
    { key: 'r', label: 'Resistance', type: 'number', unit: 'p.u.', default: 0.01 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 25, cy = y + 20;
    setStroke(ctx);
    drawLine(ctx, x + 25, y, x + 25, y + 10);
    drawLine(ctx, x + 25, y + 30, x + 25, y + 40);
    drawCircle(ctx, cx, cy, 10);
    drawFilledCircle(ctx, cx, cy, 3);
  },
};

export const transformer3WSymbol: IECSymbol = {
  type: 'transformer-3w',
  name: 'Three-Winding Transformer',
  ieeeSymbol: 'IEEE 315 11-6-3',
  category: 'transmission',
  width: 60,
  height: 60,
  connectionPoints: [
    { id: 'top', x: 30, y: 0, type: 'top' },
    { id: 'left', x: 0, y: 30, type: 'left' },
    { id: 'right', x: 60, y: 30, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 100 },
    { key: 'tap', label: 'Tap Position', type: 'number', default: 0 },
    { key: 'vectorGroup', label: 'Vector Group', type: 'string', default: 'Dyn11' },
    { key: 'v1', label: 'Winding 1', type: 'number', unit: 'kV', default: 230 },
    { key: 'v2', label: 'Winding 2', type: 'number', unit: 'kV', default: 138 },
    { key: 'v3', label: 'Winding 3', type: 'number', unit: 'kV', default: 69 },
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 30;
    setStroke(ctx);
    drawLine(ctx, x + 30, y, x + 30, y + 10);
    drawLine(ctx, x, y + 30, x + 10, y + 30);
    drawLine(ctx, x + 30, y + 50, x + 30, y + 60);
    drawCircle(ctx, cx, cy, 15);
    drawCircle(ctx, cx, cy, 8);
    drawFilledCircle(ctx, cx, cy, 3);
  },
};

export const transformerRegSymbol: IECSymbol = {
  type: 'transformer-reg',
  name: 'Regulating Transformer',
  ieeeSymbol: 'IEEE 315',
  category: 'transmission',
  width: 60,
  height: 40,
  connectionPoints: [
    { id: 'left', x: 0, y: 20, type: 'left' },
    { id: 'right', x: 60, y: 20, type: 'right' },
  ],
  properties: [
    { key: 'name', label: 'Name', type: 'string' },
    { key: 'rating', label: 'Rating', type: 'number', unit: 'MVA', default: 50 },
    { key: 'tap', label: 'Tap Position', type: 'number', default: 0 },
    { key: 'vectorGroup', label: 'Vector Group', type: 'string', default: 'Dyn11' },
    { key: 'v', label: 'Voltage', type: 'number', unit: 'kV', default: 138 },
    { key: 'tap', label: 'Tap Position', type: 'number', default: 0 },
    { key: 'vectorGroup', label: 'Vector Group', type: 'string', default: 'Dyn11' },
  ],
  render: (ctx, x, y) => {
    const cx = x + 30, cy = y + 20;
    setStroke(ctx);
    drawLine(ctx, x, y + 20, x + 15, y + 20);
    drawLine(ctx, x + 45, y + 20, x + 60, y + 20);
    drawCircle(ctx, cx, cy, 12);
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('↕', cx, cy + 4);
  },
};
