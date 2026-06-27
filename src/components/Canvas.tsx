'use client';

import { useRef, useEffect, useState, useCallback } from 'react';
import { Bus, Line, PowerSystem, BusType } from '@/types';
import { renderSymbol } from '@/lib/symbols';

interface CanvasProps {
  system: PowerSystem;
  selectedBus: string | null;
  selectedLine: string | null;
  onSelectBus: (busId: string | null) => void;
  onSelectLine: (lineId: string | null) => void;
  onUpdateBusPosition?: (busId: string, x: number, y: number) => void;
  powerFlowResults?: any;
  // Add-mode props
  mode?: string;
  onAddBus?: (x: number, y: number, type: BusType) => void;
  onAddGenerator?: (busId: string) => void;
  onAddLoad?: (busId: string) => void;
  onAddShunt?: (busId: string) => void;
  onAddLine?: (from: string, to: string) => void;
  onAddTransformer?: (from: string, to: string) => void;
  onCancelMode?: () => void;
  addOutput?: (msg: string) => void;
}

export default function Canvas({
  system,
  selectedBus,
  selectedLine,
  onSelectBus,
  onSelectLine,
  onUpdateBusPosition,
  powerFlowResults,
  mode = 'select',
  onAddBus,
  onAddGenerator,
  onAddLoad,
  onAddShunt,
  onAddLine,
  onAddTransformer,
  onCancelMode,
  addOutput
}: CanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragTarget, setDragTarget] = useState<string | null>(null);
  const [selectedFirstBus, setSelectedFirstBus] = useState<string | null>(null);
  
  // Get bus type from mode
  const getBusTypeFromMode = (m: string): BusType => {
    if (m === 'add-bus-slack') return 'slack';
    if (m === 'add-bus-pv') return 'pv';
    return 'pq';
  };

  const isAddMode = (m: string): boolean => {
    return m.startsWith('add-bus-') || m === 'add-line' || m === 'add-transformer' || m === 'add-generator' || m === 'add-load' || m === 'add-shunt';
  };

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
    
    // Draw buses with PSAT/IEEE standard symbols
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
        ctx.strokeStyle = isSelected ? '#f59e0b' : color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.stroke();
      } else {
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
    
    // Draw generators attached to buses
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
      
      ctx.beginPath();
      ctx.arc(gx + 12, gy + 12, 12, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      
      ctx.fillStyle = '#22c55e';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('G', gx + 12, gy + 13);
      
      ctx.fillStyle = '#1f2937';
      ctx.font = '8px sans-serif';
      ctx.textBaseline = 'alphabetic';
      ctx.fillText(gen.name || 'Gen', gx + 12, gy + 32);
      
      ctx.restore();
    });
    
    // Draw loads attached to buses
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
      
      ctx.beginPath();
      ctx.moveTo(lx + 12, ly);
      ctx.lineTo(lx + 12, ly + 24);
      ctx.stroke();
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(lx + 4, ly + 12);
      ctx.lineTo(lx + 20, ly + 12);
      ctx.stroke();
      
      ctx.fillStyle = '#1f2937';
      ctx.lineWidth = 1;
      ctx.font = '8px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(load.name || 'Load', lx + 12, ly + 35);
      
      ctx.restore();
    });
    
    // Draw mode preview/instructions
    if (isAddMode(mode)) {
      ctx.fillStyle = '#2563eb';
      ctx.font = 'bold 14px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'bottom';
      
      let instruction = '';
      if (mode.startsWith('add-bus-')) {
        instruction = `Click to add ${mode.replace('add-bus-', '').toUpperCase()} Bus (Press ESC to cancel)`;
      } else if (mode === 'add-line') {
        instruction = selectedFirstBus ? 'Click second bus to add Line (Press ESC to cancel)' : 'Click first bus to start Line (Press ESC to cancel)';
      } else if (mode === 'add-transformer') {
        instruction = selectedFirstBus ? 'Click second bus for Transformer (Press ESC to cancel)' : 'Click first bus for Transformer (Press ESC to cancel)';
      } else if (mode === 'add-generator') {
        instruction = 'Click a bus to attach Generator (Press ESC to cancel)';
      } else if (mode === 'add-load') {
        instruction = 'Click a bus to attach Load (Press ESC to cancel)';
      } else if (mode === 'add-shunt') {
        instruction = 'Click a bus to attach Shunt (Press ESC to cancel)';
      }
      
      // Draw instruction at top
      ctx.save();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = 'rgba(37, 99, 235, 0.1)';
      ctx.fillRect(0, 0, width, 40);
      ctx.fillStyle = '#2563eb';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(instruction, width / 2, 28);
      ctx.restore();
    }
    
    ctx.restore();
  }, [system, scale, offset, selectedBus, selectedLine, powerFlowResults, mode, selectedFirstBus]);
  
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
  
  const handleCanvasClick = (e: React.MouseEvent) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Convert to world coordinates
    const canvasW = canvasRef.current?.width || rect.width;
    const canvasH = canvasRef.current?.height || rect.height;
    const worldX = (x - canvasW / 2 - offset.x) / scale;
    const worldY = (y - canvasH / 2 - offset.y) / scale;
    
    // Find which bus was clicked (if any)
    let clickedBusId: string | null = null;
    for (const bus of system.buses) {
      const dx = worldX - bus.x * 100;
      const dy = worldY - bus.y * 100;
      if (Math.sqrt(dx * dx + dy * dy) < 25) {
        clickedBusId = bus.id;
        break;
      }
    }
    
    // Handle add modes
    if (mode.startsWith('add-bus-') && onAddBus) {
      const busType = getBusTypeFromMode(mode);
      const posX = Math.round(worldX / 50) * 50 / 100; // Snap to grid (0.5 increments)
      const posY = Math.round(worldY / 50) * 50 / 100;
      onAddBus(Math.max(0, posX), Math.max(0, posY), busType);
      if (addOutput) addOutput(`Added ${busType.toUpperCase()} bus`);
      if (onCancelMode) onCancelMode();
      return;
    }
    
    if ((mode === 'add-generator' || mode === 'add-load' || mode === 'add-shunt') && clickedBusId) {
      if (mode === 'add-generator' && onAddGenerator) {
        onAddGenerator(clickedBusId);
        if (addOutput) addOutput(`Generator added to bus ${clickedBusId}`);
      } else if (mode === 'add-load' && onAddLoad) {
        onAddLoad(clickedBusId);
        if (addOutput) addOutput(`Load added to bus ${clickedBusId}`);
      } else if (mode === 'add-shunt' && onAddShunt) {
        onAddShunt(clickedBusId);
        if (addOutput) addOutput(`Shunt added to bus ${clickedBusId}`);
      }
      if (onCancelMode) onCancelMode();
      return;
    }
    
    if ((mode === 'add-line' || mode === 'add-transformer') && clickedBusId) {
      if (!selectedFirstBus) {
        setSelectedFirstBus(clickedBusId);
        if (addOutput) addOutput(`Selected bus ${clickedBusId} as start point`);
        return;
      }
      
      if (clickedBusId !== selectedFirstBus) {
        if (mode === 'add-line' && onAddLine) {
          onAddLine(selectedFirstBus, clickedBusId);
          if (addOutput) addOutput(`Line added between ${selectedFirstBus} and ${clickedBusId}`);
        } else if (mode === 'add-transformer' && onAddTransformer) {
          onAddTransformer(selectedFirstBus, clickedBusId);
          if (addOutput) addOutput(`Transformer added between ${selectedFirstBus} and ${clickedBusId}`);
        }
      }
      
      setSelectedFirstBus(null);
      if (onCancelMode) onCancelMode();
      return;
    }
  };
  
  const handleMouseDown = (e: React.MouseEvent) => {
    // In add mode, clicking adds components instead of selecting
    if (mode !== 'select') {
      handleCanvasClick(e);
      return;
    }
    
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const canvasW = canvasRef.current?.width || rect.width;
    const canvasH = canvasRef.current?.height || rect.height;
    const worldX = (x - canvasW / 2 - offset.x) / scale;
    const worldY = (y - canvasH / 2 - offset.y) / scale;
    
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
    
    const canvasW = canvasRef.current?.width || rect.width;
    const canvasH = canvasRef.current?.height || rect.height;
    const worldX = (x - canvasW / 2 - offset.x) / scale / 100;
    const worldY = (y - canvasH / 2 - offset.y) / scale / 100;
    
    onUpdateBusPosition(dragTarget, Math.max(0, worldX), Math.max(0, worldY));
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
  
  // Handle ESC key to cancel add mode
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isAddMode(mode) && onCancelMode) {
        setSelectedFirstBus(null);
        onCancelMode();
        if (addOutput) addOutput('Cancelled');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mode, onCancelMode, addOutput]);
  
  // Reset selectedFirstBus when mode changes
  useEffect(() => {
    if (!mode.startsWith('add-line') && !mode.startsWith('add-transformer')) {
      setSelectedFirstBus(null);
    }
  }, [mode]);
  
  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
      style={{ cursor: isAddMode(mode) ? 'crosshair' : 'default' }}
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