'use client';

import { useRef, useEffect, useState, useCallback } from 'react';
import { Bus, Line, PowerSystem } from '@/types';
import { renderSymbol } from '@/lib/symbols';

interface CanvasProps {
  system: PowerSystem;
  selectedBus: string | null;
  selectedLine: string | null;
  onSelectBus: (busId: string | null) => void;
  onSelectLine: (lineId: string | null) => void;
  onUpdateBusPosition?: (busId: string, x: number, y: number) => void;
  powerFlowResults?: any;
}

export default function Canvas({
  system,
  selectedBus,
  selectedLine,
  onSelectBus,
  onSelectLine,
  onUpdateBusPosition,
  powerFlowResults
}: CanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragTarget, setDragTarget] = useState<string | null>(null);
  
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);
    
    // Draw grid
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 0.5;
    const gridSize = 50 * scale;
    const offsetX = offset.x % gridSize;
    const offsetY = offset.y % gridSize;
    
    for (let x = offsetX; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = offsetY; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    
    ctx.save();
    ctx.translate(width / 2 + offset.x, height / 2 + offset.y);
    ctx.scale(scale, scale);
    
    // Draw lines
    system.lines.forEach(line => {
      const fromBus = system.buses.find(b => b.id === line.fromBus);
      const toBus = system.buses.find(b => b.id === line.toBus);
      
      if (!fromBus || !toBus) return;
      
      const isSelected = line.id === selectedLine;
      const loading = powerFlowResults?.lineResults?.find((r: any) => r.id === line.id)?.loading || 0;
      
      // Color based on loading
      let color = isSelected ? '#2563eb' : '#6b7280';
      if (loading > 80) color = '#dc2626';
      else if (loading > 50) color = '#f59e0b';
      
      ctx.strokeStyle = color;
      ctx.lineWidth = isSelected ? 3 : 2;
      
      ctx.beginPath();
      ctx.moveTo(fromBus.x * 100, fromBus.y * 100);
      ctx.lineTo(toBus.x * 100, toBus.y * 100);
      ctx.stroke();
      
      // Draw loading label if results available
      if (powerFlowResults && loading > 0) {
        const midX = (fromBus.x + toBus.x) * 50;
        const midY = (fromBus.y + toBus.y) * 50;
        ctx.fillStyle = '#374151';
        ctx.font = '10px sans-serif';
        ctx.fillText(`${loading.toFixed(0)}%`, midX - 10, midY - 5);
      }
    });
    
    // Draw transformers with IEEE symbol
    system.transformers.forEach(txf => {
      const fromBus = system.buses.find(b => b.id === txf.fromBus);
      const toBus = system.buses.find(b => b.id === txf.toBus);
      
      if (!fromBus || !toBus) return;
      
      ctx.strokeStyle = selectedLine === txf.id ? '#2563eb' : '#6b7280';
      ctx.lineWidth = selectedLine === txf.id ? 3 : 2;
      
      ctx.beginPath();
      ctx.moveTo(fromBus.x * 100, fromBus.y * 100);
      ctx.lineTo(toBus.x * 100, toBus.y * 100);
      ctx.stroke();
      
      // Draw IEEE 2-winding transformer symbol at midpoint
      const midX = (fromBus.x + toBus.x) * 50;
      const midY = (fromBus.y + toBus.y) * 50;
      
      ctx.save();
      ctx.strokeStyle = selectedLine === txf.id ? '#2563eb' : '#6b7280';
      ctx.fillStyle = '#ffffff';
      ctx.lineWidth = 2;
      
      // Two concentric circles (IEEE 315 11-6-1 transformer)
      ctx.beginPath();
      ctx.arc(midX, midY, 9, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(midX, midY, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      
      ctx.restore();
    });
    
    // Draw buses with PSAT/IEEE standard symbols (horizontal bus lines)
    system.buses.forEach(bus => {
      const x = bus.x * 100;
      const y = bus.y * 100;
      const isSelected = bus.id === selectedBus;
      
      const colors = {
        slack: '#22c55e',
        pv: '#3b82f6',
        pq: '#6b7280'
      };
      const color = colors[bus.type as keyof typeof colors] || '#999';
      
      ctx.save();
      ctx.strokeStyle = isSelected ? '#f59e0b' : color;
      ctx.lineWidth = isSelected ? 4 : 3;
      ctx.fillStyle = color;
      
      // PSAT bus: thick horizontal line (standard single-line diagram)
      const busLength = 30;
      ctx.beginPath();
      ctx.moveTo(x - busLength / 2, y);
      ctx.lineTo(x + busLength / 2, y);
      ctx.stroke();
      
      // Additional markers per bus type
      if (bus.type === 'slack') {
        // Slack/Infinite bus: angled infinite bus marks
        ctx.strokeStyle = isSelected ? '#f59e0b' : color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x - busLength / 2, y);
        ctx.lineTo(x - busLength / 2 + 8, y - 10);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x - busLength / 2, y);
        ctx.lineTo(x - busLength / 2 + 8, y + 10);
        ctx.stroke();
      } else if (bus.type === 'pv') {
        // PV bus: circle on bus line (voltage controlled)
        ctx.strokeStyle = isSelected ? '#f59e0b' : color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        // PQ bus: small solid dot on bus line
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
      
      ctx.restore();
      
      // Draw voltage value if power flow results
      if (powerFlowResults) {
        const result = powerFlowResults.busResults.find((r: any) => r.id === bus.id);
        if (result) {
          ctx.fillStyle = '#374151';
          ctx.font = 'bold 11px monospace';
          ctx.textAlign = 'center';
          ctx.fillText(result.voltage.toFixed(3), x, y - 12);
        }
      }
      
      // Draw bus name
      ctx.fillStyle = '#1f2937';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(bus.name, x, y - 22);
      
      // Draw bus ID
      ctx.fillStyle = '#6b7280';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`#${bus.id}`, x, y + 18);
    });
    
    // Draw generators attached to buses (PSAT standard: circle with G)
    (system.generators || []).forEach(gen => {
      const bus = system.buses.find(b => b.id === gen.bus);
      if (!bus) return;
      
      const bx = bus.x * 100;
      const by = bus.y * 100;
      const gx = bx - 35;
      const gy = by - 20;
      
      ctx.save();
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2;
      ctx.fillStyle = '#ffffff';
      
      // PSAT generator: circle with G inside
      ctx.beginPath();
      ctx.arc(gx + 12, gy + 12, 12, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      
      ctx.fillStyle = '#22c55e';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('G', gx + 12, gy + 13);
      
      // Generator label below
      ctx.fillStyle = '#1f2937';
      ctx.font = '8px sans-serif';
      ctx.textBaseline = 'alphabetic';
      ctx.fillText(gen.name || 'Gen', gx + 12, gy + 32);
      
      ctx.restore();
    });
    
    // Draw loads attached to buses (PSAT standard: downward arrow/line)
    (system.loads || []).forEach(load => {
      const bus = system.buses.find(b => b.id === load.bus);
      if (!bus) return;
      
      const bx = bus.x * 100;
      const by = bus.y * 100;
      const lx = bx + 35;
      const ly = by - 20;
      
      ctx.save();
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 2;
      ctx.fillStyle = '#dc2626';
      
      // PSAT load: vertical line with thick horizontal crossbar (arrow/downward style)
      ctx.beginPath();
      ctx.moveTo(lx + 12, ly);
      ctx.lineTo(lx + 12, ly + 24);
      ctx.stroke();
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(lx + 4, ly + 12);
      ctx.lineTo(lx + 20, ly + 12);
      ctx.stroke();
      
      // Load label below
      ctx.fillStyle = '#1f2937';
      ctx.lineWidth = 1;
      ctx.font = '8px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(load.name || 'Load', lx + 12, ly + 35);
      
      ctx.restore();
    });
    
    ctx.restore();
  }, [system, scale, offset, selectedBus, selectedLine, powerFlowResults]);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const resizeCanvas = () => {
      canvas.width = canvas.parentElement?.clientWidth || 800;
      canvas.height = canvas.parentElement?.clientHeight || 600;
      draw();
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    return () => window.removeEventListener('resize', resizeCanvas);
  }, [draw]);
  
  const handleMouseDown = (e: React.MouseEvent) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Convert to world coordinates
    const worldX = (x - rect.width / 2 - offset.x) / scale;
    const worldY = (y - rect.height / 2 - offset.y) / scale;
    
    // Check if clicking on a bus
    for (const bus of system.buses) {
      const dx = worldX - bus.x * 100;
      const dy = worldY - bus.y * 100;
      if (Math.sqrt(dx * dx + dy * dy) < 20) {
        setIsDragging(true);
        setDragTarget(bus.id);
        onSelectBus(bus.id);
        return;
      }
    }
    
    // Check if clicking on a line
    for (const line of system.lines) {
      const fromBus = system.buses.find(b => b.id === line.fromBus);
      const toBus = system.buses.find(b => b.id === line.toBus);
      if (!fromBus || !toBus) continue;
      
      const dist = pointToLineDistance(
        worldX, worldY,
        fromBus.x * 100, fromBus.y * 100,
        toBus.x * 100, toBus.y * 100
      );
      
      if (dist < 10) {
        onSelectLine(line.id);
        onSelectBus(null);
        return;
      }
    }
    
    onSelectBus(null);
    onSelectLine(null);
  };
  
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging || !dragTarget || !onUpdateBusPosition) return;
    
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const worldX = (x - rect.width / 2 - offset.x) / scale / 100;
    const worldY = (y - rect.height / 2 - offset.y) / scale / 100;
    
    onUpdateBusPosition(dragTarget, worldX, worldY);
  };
  
  const handleMouseUp = () => {
    setIsDragging(false);
    setDragTarget(null);
  };
  
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setScale(s => Math.max(0.2, Math.min(5, s * delta)));
  };
  
  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full cursor-crosshair"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
    />
  );
}

function pointToLineDistance(
  px: number, py: number,
  x1: number, y1: number,
  x2: number, y2: number
): number {
  const A = px - x1;
  const B = py - y1;
  const C = x2 - x1;
  const D = y2 - y1;
  
  const dot = A * C + B * D;
  const lenSq = C * C + D * D;
  let param = -1;
  
  if (lenSq !== 0) param = dot / lenSq;
  
  let xx, yy;
  if (param < 0) {
    xx = x1;
    yy = y1;
  } else if (param > 1) {
    xx = x2;
    yy = y2;
  } else {
    xx = x1 + param * C;
    yy = y1 + param * D;
  }
  
  const dx = px - xx;
  const dy = py - yy;
  return Math.sqrt(dx * dx + dy * dy);
}