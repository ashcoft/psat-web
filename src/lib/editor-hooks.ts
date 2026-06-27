/**
 * Graphical Editor Hooks
 * Custom hooks for the power system editor
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { 
  PowerSystem, 
  Bus, 
  Line, 
  Generator, 
  Load,
  Transformer,
  Shunt
} from '@/types';

// Selection state
export interface SelectionState {
  type: 'bus' | 'line' | 'generator' | 'load' | 'transformer' | 'shunt' | null;
  id: string | null;
}

// Editor mode
export type EditorMode = 'select' | 'pan' | 'add-bus-slack' | 'add-bus-pv' | 'add-bus-pq' | 'add-line' | 'add-transformer' | 'add-generator' | 'add-load' | 'add-shunt' | 'delete';

// Grid settings
export interface GridSettings {
  show: boolean;
  snap: boolean;
  size: number;
  color: string;
}

// History for undo/redo
export interface HistoryEntry {
  system: PowerSystem;
  description: string;
}

// Editor state
export interface EditorState {
  system: PowerSystem;
  selection: SelectionState;
  mode: EditorMode;
  zoom: number;
  pan: { x: number; y: number };
  grid: GridSettings;
  lineStartBus: string | null;
  clipboard: PowerSystem | null;
}

/**
 * Main editor hook
 */
export function useEditor(initialSystem?: PowerSystem) {
  const [state, setState] = useState<EditorState>({
    system: initialSystem || createEmptySystem(),
    selection: { type: null, id: null },
    mode: 'select',
    zoom: 1,
    pan: { x: 0, y: 0 },
    grid: { show: true, snap: true, size: 20, color: '#e0e0e0' },
    lineStartBus: null,
    clipboard: null
  });

  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  // Use refs for state to avoid dependency issues - update via effect
  const stateRef = useRef(state);
  useEffect(() => {
    stateRef.current = state;
  });

  // Save to history
  const saveToHistory = useCallback((description: string) => {
    setState(prev => {
      const newEntry: HistoryEntry = {
        system: JSON.parse(JSON.stringify(prev.system)),
        description
      };
      
      const newHistory = history.slice(0, historyIndex + 1);
      newHistory.push(newEntry);
      
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
      
      return prev;
    });
  }, [history, historyIndex]);

  // Undo
  const undo = useCallback(() => {
    if (historyIndex > 0) {
      const prevEntry = history[historyIndex - 1];
      setState(prev => ({
        ...prev,
        system: JSON.parse(JSON.stringify(prevEntry.system))
      }));
      setHistoryIndex(historyIndex - 1);
    }
  }, [history, historyIndex]);

  // Redo
  const redo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const nextEntry = history[historyIndex + 1];
      setState(prev => ({
        ...prev,
        system: JSON.parse(JSON.stringify(nextEntry.system))
      }));
      setHistoryIndex(historyIndex + 1);
    }
  }, [history, historyIndex]);

  // Add bus
  const addBus = useCallback((x: number, y: number, type: Bus['type'] = 'pq') => {
    saveToHistory('Add bus');
    setState(prev => {
      const id = `bus_${Date.now()}`;
      const newBus: Bus = {
        id,
        name: `Bus ${prev.system.buses.length + 1}`,
        type,
        voltage: type === 'slack' ? 1.0 : type === 'pv' ? 1.05 : 1.0,
        angle: 0,
        vmin: 0.9,
        vmax: 1.1,
        area: 1,
        region: 1,
        x,
        y,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          buses: [...prev.system.buses, newBus]
        },
        selection: { type: 'bus', id },
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Add line
  const addLine = useCallback((fromBus: string, toBus: string) => {
    if (fromBus === toBus) return;
    
    saveToHistory('Add line');
    setState(prev => {
      const id = `line_${Date.now()}`;
      const newLine: Line = {
        id,
        fromBus,
        toBus,
        resistance: 0.01,
        reactance: 0.04,
        susceptance: 0,
        rating: 100,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          lines: [...prev.system.lines, newLine]
        },
        lineStartBus: null,
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Add generator
  const addGenerator = useCallback((busId: string) => {
    saveToHistory('Add generator');
    setState(prev => {
      const id = `gen_${Date.now()}`;
      const newGen: Generator = {
        id,
        bus: busId,
        pg: 0.5,
        qg: 0,
        v: 1.0,
        pmax: 1.0,
        pmin: 0,
        qmax: 0.5,
        qmin: -0.5,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          generators: [...prev.system.generators, newGen]
        },
        selection: { type: 'generator', id },
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Add load
  const addLoad = useCallback((busId: string) => {
    saveToHistory('Add load');
    setState(prev => {
      const id = `load_${Date.now()}`;
      const newLoad: Load = {
        id,
        bus: busId,
        pl: 0.5,
        ql: 0.2,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          loads: [...prev.system.loads, newLoad]
        },
        selection: { type: 'load', id },
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Add transformer
  const addTransformer = useCallback((fromBus: string, toBus: string) => {
    if (fromBus === toBus) return;
    
    saveToHistory('Add transformer');
    setState(prev => {
      const id = `txf_${Date.now()}`;
      const newTxf: Transformer = {
        id,
        fromBus,
        toBus,
        resistance: 0.01,
        reactance: 0.05,
        tap: 1.0,
        shift: 0,
        rating: 100,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          transformers: [...(prev.system.transformers || []), newTxf]
        },
        lineStartBus: null,
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Add shunt
  const addShunt = useCallback((busId: string) => {
    saveToHistory('Add shunt');
    setState(prev => {
      const id = `shunt_${Date.now()}`;
      const newShunt: Shunt = {
        id,
        bus: busId,
        g: 0,
        b: 0.1,
        active: true
      };
      
      return {
        ...prev,
        system: {
          ...prev.system,
          shunts: [...(prev.system.shunts || []), newShunt]
        },
        selection: { type: 'shunt', id },
        mode: 'select'
      };
    });
  }, [saveToHistory]);

  // Update component functions
  const updateBus = useCallback((busId: string, updatedBus: Partial<Bus>) => {
    saveToHistory('Update bus');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        buses: prev.system.buses.map(b => b.id === busId ? { ...b, ...updatedBus } : b)
      }
    }));
  }, [saveToHistory]);

  const updateLine = useCallback((lineId: string, updatedLine: Partial<Line>) => {
    saveToHistory('Update line');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        lines: prev.system.lines.map(l => l.id === lineId ? { ...l, ...updatedLine } : l)
      }
    }));
  }, [saveToHistory]);

  const updateGenerator = useCallback((genId: string, updatedGen: Partial<Generator>) => {
    saveToHistory('Update generator');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        generators: prev.system.generators.map(g => g.id === genId ? { ...g, ...updatedGen } : g)
      }
    }));
  }, [saveToHistory]);

  const updateLoad = useCallback((loadId: string, updatedLoad: Partial<Load>) => {
    saveToHistory('Update load');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        loads: prev.system.loads.map(l => l.id === loadId ? { ...l, ...updatedLoad } : l)
      }
    }));
  }, [saveToHistory]);

  const updateTransformer = useCallback((txfId: string, updatedTxf: Partial<Transformer>) => {
    saveToHistory('Update transformer');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        transformers: (prev.system.transformers || []).map(t => t.id === txfId ? { ...t, ...updatedTxf } : t)
      }
    }));
  }, [saveToHistory]);

  const updateShunt = useCallback((shuntId: string, updatedShunt: Partial<Shunt>) => {
    saveToHistory('Update shunt');
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        shunts: (prev.system.shunts || []).map(s => s.id === shuntId ? { ...s, ...updatedShunt } : s)
      }
    }));
  }, [saveToHistory]);

  // Delete selected element
  const deleteSelected = useCallback(() => {
    const selection = stateRef.current.selection;
    if (!selection.type || !selection.id) return;
    
    saveToHistory('Delete element');
    setState(prev => {
      let newSystem = { ...prev.system };
      
      switch (selection.type) {
        case 'bus':
          // Remove bus and all connected components
          newSystem = {
            ...newSystem,
            buses: newSystem.buses.filter(b => b.id !== selection.id),
            lines: newSystem.lines.filter(l => l.fromBus !== selection.id && l.toBus !== selection.id),
            transformers: (newSystem.transformers || []).filter(t => t.fromBus !== selection.id && t.toBus !== selection.id),
            generators: newSystem.generators.filter(g => g.bus !== selection.id),
            loads: newSystem.loads.filter(l => l.bus !== selection.id),
            shunts: (newSystem.shunts || []).filter(s => s.bus !== selection.id)
          };
          break;
        case 'line':
          newSystem = {
            ...newSystem,
            lines: newSystem.lines.filter(l => l.id !== selection.id)
          };
          break;
        case 'transformer':
          newSystem = {
            ...newSystem,
            transformers: (newSystem.transformers || []).filter(t => t.id !== selection.id)
          };
          break;
        case 'generator':
          newSystem = {
            ...newSystem,
            generators: newSystem.generators.filter(g => g.id !== selection.id)
          };
          break;
        case 'load':
          newSystem = {
            ...newSystem,
            loads: newSystem.loads.filter(l => l.id !== selection.id)
          };
          break;
        case 'shunt':
          newSystem = {
            ...newSystem,
            shunts: (newSystem.shunts || []).filter(s => s.id !== selection.id)
          };
          break;
      }
      
      return {
        ...prev,
        system: newSystem,
        selection: { type: null, id: null }
      };
    });
  }, [saveToHistory]);

  // Select element
  const select = useCallback((type: SelectionState['type'], id: string | null) => {
    setState(prev => ({
      ...prev,
      selection: { type, id }
    }));
  }, []);

  // Set mode
  const setMode = useCallback((mode: EditorMode) => {
    setState(prev => ({
      ...prev,
      mode,
      lineStartBus: mode === 'add-line' ? null : prev.lineStartBus
    }));
  }, []);

  // Zoom
  const zoom = useCallback((delta: number) => {
    setState(prev => ({
      ...prev,
      zoom: Math.max(0.25, Math.min(4, prev.zoom + delta))
    }));
  }, []);

  // Pan
  const pan = useCallback((dx: number, dy: number) => {
    setState(prev => ({
      ...prev,
      pan: {
        x: prev.pan.x + dx,
        y: prev.pan.y + dy
      }
    }));
  }, []);

  // Set system
  const setSystem = useCallback((system: PowerSystem) => {
    saveToHistory('Load system');
    setState(prev => ({
      ...prev,
      system
    }));
  }, [saveToHistory]);

  // Move bus
  const moveBus = useCallback((busId: string, x: number, y: number) => {
    setState(prev => ({
      ...prev,
      system: {
        ...prev.system,
        buses: prev.system.buses.map(b =>
          b.id === busId ? { ...b, x, y } : b
        )
      }
    }));
  }, []);

  // Start line drawing
  const startLineDrawing = useCallback((busId: string) => {
    setState(prev => ({
      ...prev,
      lineStartBus: busId
    }));
  }, []);

  // Complete line drawing
  const completeLineDrawing = useCallback((busId: string) => {
    const lineStartBus = stateRef.current.lineStartBus;
    if (lineStartBus) {
      addLine(lineStartBus, busId);
    }
  }, [addLine]);

  // Copy/Paste
  const copy = useCallback(() => {
    setState(prev => ({
      ...prev,
      clipboard: JSON.parse(JSON.stringify(prev.system))
    }));
  }, []);

  const paste = useCallback(() => {
    const clipboard = stateRef.current.clipboard;
    if (!clipboard) return;
    
    saveToHistory('Paste');
    setState(prev => ({
      ...prev,
      system: JSON.parse(JSON.stringify(clipboard))
    }));
  }, [saveToHistory]);

  return {
    state,
    setState,
    history,
    canUndo: historyIndex > 0,
    canRedo: historyIndex < history.length - 1,
    undo,
    redo,
    addBus,
    addLine,
    addTransformer,
    addGenerator,
    addLoad,
    addShunt,
    updateBus,
    updateLine,
    updateGenerator,
    updateLoad,
    updateTransformer,
    updateShunt,
    deleteSelected,
    select,
    setMode,
    zoom,
    pan,
    setSystem,
    moveBus,
    startLineDrawing,
    completeLineDrawing,
    copy,
    paste
  };
}

/**
 * Canvas rendering hook
 */
export function useCanvasRenderer(
  canvasRef: React.RefObject<HTMLCanvasElement>,
  state: EditorState
) {
  const { system, selection, zoom, pan, grid, lineStartBus, mode } = state;

  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear
    ctx.fillStyle = '#f5f5f5';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Apply transformations
    ctx.save();
    ctx.translate(pan.x, pan.y);
    ctx.scale(zoom, zoom);
    
    // Draw grid
    if (grid.show) {
      ctx.strokeStyle = grid.color;
      ctx.lineWidth = 0.5 / zoom;
      const startX = Math.floor(-pan.x / zoom / grid.size) * grid.size;
      const startY = Math.floor(-pan.y / zoom / grid.size) * grid.size;
      const endX = startX + canvas.width / zoom + grid.size * 2;
      const endY = startY + canvas.height / zoom + grid.size * 2;
      
      for (let x = startX; x < endX; x += grid.size) {
        ctx.beginPath();
        ctx.moveTo(x, startY);
        ctx.lineTo(x, endY);
        ctx.stroke();
      }
      for (let y = startY; y < endY; y += grid.size) {
        ctx.beginPath();
        ctx.moveTo(startX, y);
        ctx.lineTo(endX, y);
        ctx.stroke();
      }
    }
    
    // Draw lines
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2 / zoom;
    system.lines.forEach(line => {
      const fromBus = system.buses.find(b => b.id === line.fromBus);
      const toBus = system.buses.find(b => b.id === line.toBus);
      if (!fromBus || !toBus) return;
      
      ctx.beginPath();
      ctx.moveTo(fromBus.x, fromBus.y);
      ctx.lineTo(toBus.x, toBus.y);
      ctx.stroke();
      
      // Highlight if selected
      if (selection.type === 'line' && selection.id === line.id) {
        ctx.strokeStyle = '#0066ff';
        ctx.lineWidth = 4 / zoom;
        ctx.stroke();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2 / zoom;
      }
    });
    
    // Draw buses
    system.buses.forEach(bus => {
      const isSelected = selection.type === 'bus' && selection.id === bus.id;
      
      ctx.fillStyle = isSelected ? '#0066ff' : '#fff';
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 2 / zoom;
      
      ctx.beginPath();
      ctx.arc(bus.x, bus.y, 15 / zoom, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      
      // Label
      ctx.fillStyle = '#333';
      ctx.font = `${12 / zoom}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillText(bus.name, bus.x, bus.y + 25 / zoom);
    });
    
    // Draw line preview
    if (lineStartBus && mode === 'add-line') {
      const startBus = system.buses.find(b => b.id === lineStartBus);
      if (startBus) {
        ctx.strokeStyle = '#0066ff';
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(startBus.x, startBus.y);
        ctx.lineTo(startBus.x + 50, startBus.y + 50);
        ctx.stroke();
        ctx.setLineDash([]);
      }
    }
    
    ctx.restore();
  }, [canvasRef, system, selection, zoom, pan, grid, lineStartBus, mode]);

  useEffect(() => {
    render();
  }, [render]);

  return { render };
}

/**
 * Create empty power system
 */
function createEmptySystem(): PowerSystem {
  return {
    buses: [],
    lines: [],
    transformers: [],
    loads: [],
    generators: [],
    shunts: [],
    areas: [{ id: 'A1', name: 'Area 1', slackBus: '' }],
    baseMVA: 100,
    baseFreq: 60
  };
}
