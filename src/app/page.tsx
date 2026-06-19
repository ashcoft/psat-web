'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Ribbon from '@/components/Ribbon';
import Toolbar from '@/components/Toolbar';
import Sidebar from '@/components/Sidebar';
import PropertiesPanel from '@/components/PropertiesPanel';
import OutputWindow from '@/components/OutputWindow';
import SettingsDialog from '@/components/SettingsDialog';
import { PowerSystem, PowerFlowResult } from '@/types';
import { createDefaultSystem } from '@/lib/powerflow';
import '@/app/globals.css';

// Dynamically import Canvas to avoid SSR issues
const Canvas = dynamic(() => import('@/components/Canvas'), { ssr: false });

export default function Home() {
  const [system, setSystem] = useState<PowerSystem>(createDefaultSystem());
  const [selectedBus, setSelectedBus] = useState<string | null>(null);
  const [selectedLine, setSelectedLine] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('home');
  const [powerFlowResults, setPowerFlowResults] = useState<PowerFlowResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [output, setOutput] = useState<string[]>([]);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [propertiesPanelCollapsed, setPropertiesPanelCollapsed] = useState(false);
  
  // Store system ref for use in callbacks
  const systemRef = useRef(system);
  
  // Update ref when system changes
  useEffect(() => {
    systemRef.current = system;
  }, [system]);
  
  const addOutput = useCallback((message: string) => {
    setOutput(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  }, []);
  
  const handleRunPowerFlow = useCallback(async () => {
    setIsProcessing(true);
    addOutput('Starting Power Flow analysis...');
    
    // Simulate calculation delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Import power flow solver
    const { PowerFlowSolver } = await import('@/lib/powerflow');
    const solver = new PowerFlowSolver(systemRef.current);
    
    try {
      const results = solver.solve();
      setPowerFlowResults(results);
      addOutput(`Power Flow converged: ${results.converged}`);
      addOutput(`Iterations: ${results.iterations}`);
      addOutput(`Max Mismatch: ${results.maxMismatch.toExponential(3)}`);
      addOutput(`Total Losses: ${results.losses.real.toFixed(4)} MW`);
    } catch (error) {
      addOutput(`Error: ${error}`);
    }
    
    setIsProcessing(false);
  }, [addOutput]);
  
  const handleAction = useCallback((action: string) => {
    switch (action) {
      case 'power-flow':
        handleRunPowerFlow();
        break;
      case 'settings':
        setShowSettings(true);
        break;
      case 'zoom-in':
        // handled in canvas
        break;
      case 'add-bus':
        // handled in sidebar
        break;
      default:
        addOutput(`Action: ${action}`);
    }
  }, [handleRunPowerFlow, addOutput]);
  
  const handleUpdateBusPosition = (busId: string, x: number, y: number) => {
    setSystem(prev => ({
      ...prev,
      buses: prev.buses.map(bus => 
        bus.id === busId ? { ...bus, x, y } : bus
      )
    }));
  };
  
  const handleAddBus = (type: 'slack' | 'pv' | 'pq') => {
    const newId = `bus_${Date.now()}`;
    const newBus = {
      id: newId,
      name: `Bus ${system.buses.length + 1}`,
      type,
      voltage: type === 'slack' ? 1.0 : type === 'pv' ? 1.05 : 1.0,
      angle: 0,
      vmin: 0.9,
      vmax: 1.1,
      area: 1,
      region: 1,
      x: Math.random() * 5 - 2.5,
      y: Math.random() * 5 - 2.5,
      active: true
    };
    
    setSystem(prev => ({
      ...prev,
      buses: [...prev.buses, newBus]
    }));
    addOutput(`Added ${type} bus: ${newId}`);
  };
  
  const handleAddLine = () => {
    if (system.buses.length < 2) {
      addOutput('Need at least 2 buses to create a line');
      return;
    }
    const newId = `line_${Date.now()}`;
    const newLine = {
      id: newId,
      fromBus: system.buses[0].id,
      toBus: system.buses[1].id,
      resistance: 0.02,
      reactance: 0.04,
      susceptance: 0,
      rating: 100,
      active: true
    };
    
    setSystem(prev => ({
      ...prev,
      lines: [...prev.lines, newLine]
    }));
    addOutput(`Added line: ${newId}`);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Title Bar */}
      <div className="flex items-center justify-between bg-blue-700 text-white px-4 py-2 shadow-md">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold">⚡ PSAT</span>
          <span className="text-sm opacity-75">Power System Analysis Toolbox</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span>File</span>
          <span>Edit</span>
          <span>View</span>
          <span>Analysis</span>
          <span>Help</span>
        </div>
      </div>

      {/* Toolbar */}
      <Toolbar
        onNew={() => setSystem(createDefaultSystem())}
        onOpen={() => addOutput('Open dialog triggered')}
        onSave={() => addOutput('Save dialog triggered')}
        onUndo={() => addOutput('Undo')}
        onRedo={() => addOutput('Redo')}
        onZoomIn={() => {}}
        onZoomOut={() => {}}
        onFit={() => {}}
        onRunPowerFlow={handleRunPowerFlow}
        onRunTimeSim={() => addOutput('Time simulation triggered')}
        isProcessing={isProcessing}
      />

      {/* Ribbon */}
      <Ribbon
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onAction={handleAction}
      />

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        {!sidebarCollapsed && (
          <Sidebar
            system={system}
            onAddBus={handleAddBus}
            onAddLine={handleAddLine}
            onCollapse={() => setSidebarCollapsed(true)}
          />
        )}
        
        {sidebarCollapsed && (
          <button
            onClick={() => setSidebarCollapsed(false)}
            className="absolute left-0 top-1/2 bg-gray-200 px-1 py-4 rounded-r-lg shadow-md"
          >
            ▶
          </button>
        )}

        {/* Canvas Area */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 bg-white border border-gray-300 relative">
            <Canvas
              system={system}
              selectedBus={selectedBus}
              selectedLine={selectedLine}
              onSelectBus={setSelectedBus}
              onSelectLine={setSelectedLine}
              onUpdateBusPosition={handleUpdateBusPosition}
              powerFlowResults={powerFlowResults}
            />
            
            {/* Canvas controls */}
            <div className="absolute bottom-4 left-4 flex gap-2">
              <button className="p-2 bg-white rounded shadow hover:bg-gray-100" title="Pan">
                ✋
              </button>
              <button className="p-2 bg-white rounded shadow hover:bg-gray-100" title="Select">
                ↖
              </button>
              <button className="p-2 bg-white rounded shadow hover:bg-gray-100" title="Zoom">
                🔍
              </button>
            </div>
          </div>
          
          {/* Output Window */}
          <OutputWindow
            messages={output}
            onClear={() => setOutput([])}
          />
        </div>

        {/* Properties Panel */}
        {!propertiesPanelCollapsed && (
          <PropertiesPanel
            system={system}
            selectedBus={selectedBus}
            selectedLine={selectedLine}
            powerFlowResults={powerFlowResults}
            onUpdateBus={() => {}}
            onUpdateLine={() => {}}
            onCollapse={() => setPropertiesPanelCollapsed(true)}
          />
        )}
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between bg-gray-200 border-t border-gray-300 px-4 py-1 text-xs text-gray-600">
        <div className="flex items-center gap-4">
          <span>Buses: {system.buses.length}</span>
          <span>Lines: {system.lines.length}</span>
          <span>Transformers: {system.transformers.length}</span>
          <span>Loads: {system.loads.length}</span>
          <span>Generators: {system.generators.length}</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Base: 100 MVA</span>
          <span>Frequency: 50 Hz</span>
          {powerFlowResults && (
            <>
              <span className="text-green-600">✓ Converged</span>
              <span>Iterations: {powerFlowResults.iterations}</span>
            </>
          )}
        </div>
      </div>

      {/* Settings Dialog */}
      {showSettings && (
        <SettingsDialog onClose={() => setShowSettings(false)} />
      )}
    </div>
  );
}