'use client';

import { useEffect, useRef } from 'react';
import type { CPFHistory } from '@/lib/cpf';
import type { SimulationResult } from '@/types';
import type { StabilityAnalysisResult } from '@/lib/stability';

interface AnalysisChartsProps {
  activeAnalysis: 'power-flow' | 'cpf' | 'opf' | 'short-circuit' | 'transient-stability' | 'small-signal-stability';
  cpfResults: CPFHistory | null;
  timeseriesResults: any; // SimulationResult
  stabilityResults: StabilityAnalysisResult | null;
}

export default function AnalysisCharts({
  activeAnalysis,
  cpfResults,
  timeseriesResults,
  stabilityResults
}: AnalysisChartsProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width = canvas.parentElement?.clientWidth || 600;
    const height = canvas.height = canvas.parentElement?.clientHeight || 400;

    // Clear
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    if (activeAnalysis === 'cpf' && cpfResults && cpfResults.results.length > 0) {
      drawCPFCurve(ctx, width, height, cpfResults);
    } else if (activeAnalysis === 'transient-stability' && timeseriesResults && timeseriesResults.time) {
      drawTransientSwingCurve(ctx, width, height, timeseriesResults);
    } else if (activeAnalysis === 'small-signal-stability' && stabilityResults && stabilityResults.eigenvalues) {
      drawEigenvalueSPlane(ctx, width, height, stabilityResults);
    } else {
      drawNoDataMessage(ctx, width, height, activeAnalysis);
    }
  }, [activeAnalysis, cpfResults, timeseriesResults, stabilityResults]);

  // Draw message when no data is available
  function drawNoDataMessage(ctx: CanvasRenderingContext2D, w: number, h: number, type: string) {
    ctx.fillStyle = '#6b7280';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`No plot data available for ${type.replace('-', ' ')}. Run simulation first.`, w / 2, h / 2);
  }

  // Draw PV Curves (voltage vs lambda)
  function drawCPFCurve(ctx: CanvasRenderingContext2D, w: number, h: number, history: CPFHistory) {
    const margin = { top: 40, right: 120, bottom: 50, left: 60 };
    const chartW = w - margin.left - margin.right;
    const chartH = h - margin.top - margin.bottom;

    // Find bounds
    let maxLambda = 0.1;
    let minV = 0.5;
    let maxV = 1.1;

    history.results.forEach(res => {
      maxLambda = Math.max(maxLambda, res.lambda);
      Object.values(res.busVoltages).forEach(v => {
        minV = Math.min(minV, v);
        maxV = Math.max(maxV, v);
      });
    });

    minV = Math.max(0, minV - 0.05);
    maxV = Math.min(1.2, maxV + 0.05);

    // Map function
    const mapX = (x: number) => margin.left + (x / maxLambda) * chartW;
    const mapY = (y: number) => margin.top + chartH - ((y - minV) / (maxV - minV)) * chartH;

    // Draw Grid Lines & Axes
    drawGrid(ctx, margin, chartW, chartH, maxLambda, minV, maxV, 'Loading Factor (λ)', 'Voltage (pu)');

    // Draw Curves for each bus
    const busIds = Object.keys(history.results[0].busVoltages);
    const colors = ['#2563eb', '#dc2626', '#16a34a', '#d97706', '#7c3aed', '#0891b2'];

    busIds.forEach((busId, idx) => {
      const color = colors[idx % colors.length];
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();

      history.results.forEach((res, rIdx) => {
        const x = mapX(res.lambda);
        const y = mapY(res.busVoltages[busId]);
        if (rIdx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });

      ctx.stroke();

      // Legend
      ctx.fillStyle = color;
      ctx.fillRect(margin.left + chartW + 15, margin.top + idx * 20, 12, 12);
      ctx.fillStyle = '#374151';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`Bus ${busId}`, margin.left + chartW + 32, margin.top + idx * 20 + 10);
    });

    // Draw Nose Point / Limit point if present
    if (history.maximumLoadingPoint) {
      const mlp = history.maximumLoadingPoint;
      ctx.fillStyle = '#dc2626';
      ctx.font = 'bold 11px sans-serif';
      const x = mapX(mlp.lambda);
      // Plot at the average or first bus voltage collapse point
      const v = Object.values(mlp.voltages)[0] || 0.7;
      const y = mapY(v);

      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#dc2626';
      ctx.fillText(`Collapse Point (λ = ${mlp.lambda.toFixed(3)})`, x + 10, y - 5);
    }
  }

  // Draw Generator Swing Curves (delta/omega over time)
  function drawTransientSwingCurve(ctx: CanvasRenderingContext2D, w: number, h: number, sim: any) {
    const margin = { top: 40, right: 120, bottom: 50, left: 60 };
    const chartW = w - margin.left - margin.right;
    const chartH = h - margin.top - margin.bottom;

    const tMax = sim.time[sim.time.length - 1] || 5;
    let minVal = -30;
    let maxVal = 180;

    const machineAngles = sim.machineAngles || {};
    const machineKeys = Object.keys(machineAngles);
    if (machineKeys.length === 0) {
      ctx.fillStyle = '#6b7280';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('No machine angle data available', margin.left + chartW / 2, margin.top + chartH / 2);
      return;
    }

    Object.values(machineAngles).forEach((angles: any) => {
      if (!angles || !Array.isArray(angles)) return;
      angles.forEach((ang: number) => {
        const deg = ang * 180 / Math.PI;
        minVal = Math.min(minVal, deg);
        maxVal = Math.max(maxVal, deg);
      });
    });

    minVal = minVal - 10;
    maxVal = maxVal + 10;

    const mapX = (t: number) => margin.left + (t / tMax) * chartW;
    const mapY = (val: number) => margin.top + chartH - ((val - minVal) / (maxVal - minVal)) * chartH;

    // Draw grid
    drawGrid(ctx, margin, chartW, chartH, tMax, minVal, maxVal, 'Time (seconds)', 'Rotor Angle (degrees)');

    // Draw curves
    const colors = ['#2563eb', '#16a34a', '#7c3aed', '#dc2626', '#d97706'];

    machineKeys.forEach((genId, idx) => {
      const color = colors[idx % colors.length];
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      let started = false;

      sim.time.forEach((t: number, tIdx: number) => {
        const angles = machineAngles[genId];
        if (!angles || !angles[tIdx]) return;
        const val = angles[tIdx] * 180 / Math.PI;
        const x = mapX(t);
        const y = mapY(val);
        if (!started) {
          ctx.moveTo(x, y);
          started = true;
        } else {
          ctx.lineTo(x, y);
        }
      });

      if (started) ctx.stroke();

      // Legend
      ctx.fillStyle = color;
      ctx.fillRect(margin.left + chartW + 15, margin.top + idx * 20, 12, 12);
      ctx.fillStyle = '#374151';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`Gen ${genId}`, margin.left + chartW + 32, margin.top + idx * 20 + 10);
    });
  }

  // Draw Complex S-Plane Eigenvalues (real vs imaginary)
  function drawEigenvalueSPlane(ctx: CanvasRenderingContext2D, w: number, h: number, stability: any) {
    const margin = { top: 40, right: 60, bottom: 50, left: 60 };
    const chartW = w - margin.left - margin.right;
    const chartH = h - margin.top - margin.bottom;

    let minReal = -10;
    let maxReal = 5;
    let minImag = -20;
    let maxImag = 20;

    stability.eigenvalues.forEach((ev: any) => {
      minReal = Math.min(minReal, ev.eigenvalue.real);
      maxReal = Math.max(maxReal, ev.eigenvalue.real);
      minImag = Math.min(minImag, ev.eigenvalue.imag);
      maxImag = Math.max(maxImag, ev.eigenvalue.imag);
    });

    minReal = minReal - 1;
    maxReal = maxReal + 1;
    minImag = minImag - 2;
    maxImag = maxImag + 2;

    const mapX = (r: number) => margin.left + ((r - minReal) / (maxReal - minReal)) * chartW;
    const mapY = (i: number) => margin.top + chartH - ((i - minImag) / (maxImag - minImag)) * chartH;

    // Draw S-Plane Grid
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 0.5;

    // Draw y-grid (real values)
    const stepReal = (maxReal - minReal) / 5;
    for (let r = minReal; r <= maxReal; r += stepReal) {
      const x = mapX(r);
      ctx.beginPath();
      ctx.moveTo(x, margin.top);
      ctx.lineTo(x, margin.top + chartH);
      ctx.stroke();

      ctx.fillStyle = '#6b7280';
      ctx.font = '9px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(r.toFixed(1), x, margin.top + chartH + 15);
    }

    // Draw x-grid (imag values)
    const stepImag = (maxImag - minImag) / 6;
    for (let i = minImag; i <= maxImag; i += stepImag) {
      const y = mapY(i);
      ctx.beginPath();
      ctx.moveTo(margin.left, y);
      ctx.lineTo(margin.left + chartW, y);
      ctx.stroke();

      ctx.fillStyle = '#6b7280';
      ctx.font = '9px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(i.toFixed(1), margin.left - 10, y + 3);
    }

    // DRAW AXES (jω axis at real = 0, and Real axis at imag = 0)
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1.5;

    // Real = 0 axis (imaginary axis)
    if (minReal <= 0 && maxReal >= 0) {
      const zeroX = mapX(0);
      ctx.beginPath();
      ctx.moveTo(zeroX, margin.top);
      ctx.lineTo(zeroX, margin.top + chartH);
      ctx.stroke();
      ctx.fillStyle = '#374151';
      ctx.font = 'bold 10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('jω axis', zeroX, margin.top - 10);
    }

    // Imag = 0 axis (real axis)
    if (minImag <= 0 && maxImag >= 0) {
      const zeroY = mapY(0);
      ctx.beginPath();
      ctx.moveTo(margin.left, zeroY);
      ctx.lineTo(margin.left + chartW, zeroY);
      ctx.stroke();
      ctx.fillStyle = '#374151';
      ctx.font = 'bold 10px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('Real axis (σ)', margin.left + chartW + 8, zeroY + 3);
    }

    // Plot eigenvalues
    stability.eigenvalues.forEach((ev: any) => {
      const x = mapX(ev.eigenvalue.real);
      const y = mapY(ev.eigenvalue.imag);
      const isUnstable = ev.eigenvalue.real > 0;

      ctx.fillStyle = isUnstable ? '#dc2626' : '#2563eb';
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();

      // Draw border
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.0;
      ctx.stroke();
    });

    // Unstable zone label
    if (maxReal > 0) {
      const zeroX = mapX(0);
      ctx.fillStyle = 'rgba(220, 38, 38, 0.05)';
      ctx.fillRect(zeroX, margin.top, margin.left + chartW - zeroX, chartH);
      
      ctx.fillStyle = '#dc2626';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('Unstable region', margin.left + chartW - 10, margin.top + 20);
    }
  }

  // Common grid helper
  function drawGrid(
    ctx: CanvasRenderingContext2D,
    margin: { top: number; right: number; bottom: number; left: number },
    w: number, h: number,
    xMax: number, yMin: number, yMax: number,
    xLabel: string, yLabel: string
  ) {
    ctx.strokeStyle = '#f3f4f6';
    ctx.lineWidth = 1;

    // Grid lines for X-axis (time or lambda)
    const stepX = xMax / 5;
    for (let xVal = 0; xVal <= xMax; xVal += stepX) {
      const cx = margin.left + (xVal / xMax) * w;
      ctx.beginPath();
      ctx.moveTo(cx, margin.top);
      ctx.lineTo(cx, margin.top + h);
      ctx.stroke();

      ctx.fillStyle = '#4b5563';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(xVal.toFixed(2), cx, margin.top + h + 15);
    }

    // Grid lines for Y-axis (voltage or angle)
    const stepY = (yMax - yMin) / 5;
    for (let yVal = yMin; yVal <= yMax; yVal += stepY) {
      const cy = margin.top + h - ((yVal - yMin) / (yMax - yMin)) * h;
      ctx.beginPath();
      ctx.moveTo(margin.left, cy);
      ctx.lineTo(margin.left + w, cy);
      ctx.stroke();

      ctx.fillStyle = '#4b5563';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(yVal.toFixed(2), margin.left - 10, cy + 3);
    }

    // Draw outer frame
    ctx.strokeStyle = '#9ca3af';
    ctx.lineWidth = 1;
    ctx.strokeRect(margin.left, margin.top, w, h);

    // X Axis Label
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(xLabel, margin.left + w / 2, margin.top + h + 35);

    // Y Axis Label
    ctx.save();
    ctx.translate(margin.left - 40, margin.top + h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(yLabel, 0, 0);
    ctx.restore();
  }

  return (
    <div className="flex-1 flex flex-col p-4 bg-gray-50 overflow-hidden h-full">
      <div className="bg-white border border-gray-300 rounded-lg shadow-sm p-4 flex-1 flex items-center justify-center relative min-h-[350px]">
        <canvas ref={canvasRef} className="max-w-full max-h-full" />
      </div>
    </div>
  );
}
