'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Ribbon from '@/components/Ribbon';
import Toolbar from '@/components/Toolbar';
import Sidebar from '@/components/Sidebar';
import PropertiesPanel from '@/components/PropertiesPanel';
import OutputWindow from '@/components/OutputWindow';
import SettingsDialog from '@/components/SettingsDialog';
import AnalysisCharts from '@/components/AnalysisCharts';
import TabularReports from '@/components/TabularReports';
import { PowerSystem, PowerFlowResult, SimulationResult } from '@/types';
import type { CPFHistory } from '@/lib/cpf';
import type { OPFResult } from '@/lib/opf';
import type { FaultStudyResult } from '@/lib/fault';
import type { StabilityAnalysisResult } from '@/lib/stability';
import { createDefaultSystem } from '@/lib/powerflow';
import { useEditor } from '@/lib/editor-hooks';
import '@/app/globals.css';

// Dynamically import Canvas to avoid SSR issues
const Canvas = dynamic(() => import('@/components/Canvas'), { ssr: false });

export default function Home() {
  const editor = useEditor(createDefaultSystem());
  const {
    state: editorState,
    undo,
    redo,
    zoom,
    select,
    setMode,
    setSystem,
    moveBus,
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
    deleteSelected
  } = editor;

  const system = editorState.system;
  
  const selectedBus = editorState.selection.type === 'bus' ? editorState.selection.id : null;
  const selectedLine = editorState.selection.type === 'line' ? editorState.selection.id : null;

  const [activeTab, setActiveTab] = useState('home');
  const [activeCenterTab, setActiveCenterTab] = useState<'canvas' | 'charts' | 'reports'>('canvas');
  
  // Results states
  const [powerFlowResults, setPowerFlowResults] = useState<PowerFlowResult | null>(null);
  const [cpfResults, setCpfResults] = useState<CPFHistory | null>(null);
  const [opfResults, setOpfResults] = useState<OPFResult | null>(null);
  const [faultResults, setFaultResults] = useState<FaultStudyResult | null>(null);
  const [timeseriesResults, setTimeseriesResults] = useState<any>(null); // SimulationResult
  const [stabilityResults, setStabilityResults] = useState<StabilityAnalysisResult | null>(null);

  const [activeAnalysis, setActiveAnalysis] = useState<'power-flow' | 'cpf' | 'opf' | 'short-circuit' | 'transient-stability' | 'small-signal-stability'>('power-flow');
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [output, setOutput] = useState<string[]>([]);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [propertiesPanelCollapsed, setPropertiesPanelCollapsed] = useState(false);

  const [settings, setSettings] = useState({
    baseFrequency: 60,
    basePower: 100,
    tolerance: 1e-6,
    maxIterations: 100,
    solutionMethod: 'nr' as 'nr' | 'dc' | 'fast-decoupled',
    flatStart: true,
    beeps: false,
    theme: 'light' as 'light' | 'dark' | 'custom',
    voltageMin: 0.9,
    voltageMax: 1.1,
  });

  const addOutput = useCallback((message: string) => {
    setOutput(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  }, []);

  // System ref for async callbacks
  const systemRef = useRef(system);
  useEffect(() => {
    systemRef.current = system;
  }, [system]);

  const handleRunAnalysis = useCallback(async () => {
    setIsProcessing(true);
    addOutput(`Starting ${activeAnalysis.replace('-', ' ')} analysis...`);

    // Simulate delay
    await new Promise(resolve => setTimeout(resolve, 800));

    try {
      if (activeAnalysis === 'power-flow') {
        const { solvePowerFlow } = await import('@/lib/powerflow-methods');
        const methodMap = {
          'nr': 'Newton-Raphson',
          'dc': 'DC',
          'fast-decoupled': 'Fast-Decoupled'
        } as const;
        const method = methodMap[settings.solutionMethod] || 'Newton-Raphson';
        const results = solvePowerFlow(systemRef.current, method);
        setPowerFlowResults(results);
        addOutput(`Power Flow (${method}) converged: ${results.converged}`);
        addOutput(`Iterations: ${results.iterations}`);
        addOutput(`Max Mismatch: ${results.maxMismatch.toExponential(3)}`);
        addOutput(`Total Losses: ${results.losses.real.toFixed(4)} MW`);
        
        setActiveCenterTab('canvas');
      } else if (activeAnalysis === 'cpf') {
        const { runCPF } = await import('@/lib/cpf');
        const results = runCPF(systemRef.current, {
          tolerance: settings.tolerance,
          maxIterations: settings.maxIterations
        });
        setCpfResults(results);
        addOutput(`Continuation Power Flow completed.`);
        addOutput(`Maximum Loading Factor (Lambda): ${results.maximumLoadingPoint?.lambda.toFixed(4) || 'N/A'}`);
        if (results.nosePoint) {
          addOutput(`Voltage Collapse Nose Point found.`);
        }
        
        setActiveCenterTab('charts');
      } else if (activeAnalysis === 'opf') {
        const { solveACOPF, solveDCOPF } = await import('@/lib/opf');
        const results = settings.solutionMethod === 'dc' ? solveDCOPF(systemRef.current) : solveACOPF(systemRef.current);
        setOpfResults(results);
        addOutput(`Optimal Power Flow completed.`);
        addOutput(`OPF Success: ${results.success}`);
        addOutput(`Total Generation Cost: $${results.totalCost.toFixed(2)}/h`);
        if (results.losses !== undefined) {
          addOutput(`System Losses: ${results.losses.toFixed(4)} MW`);
        }
        
        setActiveCenterTab('canvas');
      } else if (activeAnalysis === 'short-circuit') {
        const { performFaultStudy } = await import('@/lib/fault');
        const results = performFaultStudy(systemRef.current);
        setFaultResults(results);
        addOutput(`Short Circuit Symmetrical and Unsymmetrical Fault Study completed.`);
        addOutput(`Buses analyzed: LG, LL, LLG, 3-Phase faults.`);
        if (results.threePhaseFaults.length > 0) {
          addOutput(`Max 3-Phase Fault Current: ${results.threePhaseFaults[0].faultMVA.toFixed(2)} MVA`);
        }
        
        setActiveCenterTab('reports');
      } else if (activeAnalysis === 'transient-stability') {
        const { runTimeDomainSimulation } = await import('@/lib/timeseries');
        const results = runTimeDomainSimulation(systemRef.current);
        setTimeseriesResults(results);
        addOutput(`Transient Stability Dynamic Swing Curve Simulation completed.`);
        addOutput(`Steps simulated: ${results.time.length}`);
        
        setActiveCenterTab('charts');
      } else if (activeAnalysis === 'small-signal-stability') {
        const { analyzeSmallSignalStability } = await import('@/lib/stability');
        const results = analyzeSmallSignalStability(systemRef.current);
        setStabilityResults(results);
        addOutput(`Small Signal Stability eigenvalue analysis completed.`);
        addOutput(`Total modes: ${results.eigenvalues.length}`);
        addOutput(`Unstable modes: ${results.unstableModes.length}`);
        if (results.leastDampedMode) {
          addOutput(`Least damped: ${results.leastDampedMode.dampingRatio.toFixed(4)} damping @ ${results.leastDampedMode.frequency.toFixed(2)} Hz`);
        }
        
        setActiveCenterTab('charts');
      }
    } catch (error) {
      addOutput(`Error: ${error}`);
      console.error(error);
    }

    setIsProcessing(false);
  }, [activeAnalysis, settings, addOutput]);

  const handleAction = useCallback((action: string) => {
    switch (action) {
      case 'power-flow':
        setActiveAnalysis('power-flow');
        // Let it run
        setTimeout(() => handleRunAnalysis(), 100);
        break;
      case 'cpf':
        setActiveAnalysis('cpf');
        setTimeout(() => handleRunAnalysis(), 100);
        break;
      case 'opf':
        setActiveAnalysis('opf');
        setTimeout(() => handleRunAnalysis(), 100);
        break;
      case 'time-sim':
        setActiveAnalysis('transient-stability');
        setTimeout(() => handleRunAnalysis(), 100);
        break;
      case 'eigenvalue':
      case 'modal':
        setActiveAnalysis('small-signal-stability');
        setTimeout(() => handleRunAnalysis(), 100);
        break;
      case 'settings':
        setShowSettings(true);
        break;
      case 'undo':
        undo();
        addOutput('Undo operation');
        break;
      case 'redo':
        redo();
        addOutput('Redo operation');
        break;
      case 'zoom-in':
        zoom(0.1);
        break;
      case 'zoom-out':
        zoom(-0.1);
        break;
      case 'fit':
        editorState.zoom = 1;
        editorState.pan = { x: 0, y: 0 };
        addOutput('Zoom reset to Fit');
        break;
        
      // Component adding actions from Ribbon
      case 'add-slack':
        setMode('add-bus-slack');
        addOutput('Mode: Click Canvas to add a Slack Bus');
        break;
      case 'add-pv':
        setMode('add-bus-pv');
        addOutput('Mode: Click Canvas to add a PV Bus');
        break;
      case 'add-pq':
        setMode('add-bus-pq');
        addOutput('Mode: Click Canvas to add a PQ Bus');
        break;
      case 'add-line':
        setMode('add-line');
        addOutput('Mode: Click start bus and end bus on Canvas to add a Line');
        break;
      case 'add-transformer':
        setMode('add-transformer');
        addOutput('Mode: Click start bus and end bus on Canvas to add a Transformer');
        break;
      case 'add-generator':
        setMode('add-generator');
        addOutput('Mode: Click a bus on Canvas to attach a Generator');
        break;
      case 'add-load':
        setMode('add-load');
        addOutput('Mode: Click a bus on Canvas to attach a Load');
        break;
      case 'add-shunt':
        setMode('add-shunt');
        addOutput('Mode: Click a bus on Canvas to attach a Shunt');
        break;
      case 'report':
      case 'summary':
        setActiveCenterTab('reports');
        break;
      default:
        addOutput(`Action: ${action}`);
    }
  }, [handleRunAnalysis, undo, redo, zoom, editorState, setMode, addOutput]);

  const handleUpdateBusPosition = (busId: string, x: number, y: number) => {
    moveBus(busId, x, y);
  };

  const handleAddBusFromSidebar = (type: 'slack' | 'pv' | 'pq') => {
    setMode(`add-bus-${type}` as any);
    addOutput(`Mode: Click Canvas to add a ${type.toUpperCase()} Bus`);
  };

  return (
    <div className={`flex flex-col h-screen ${settings.theme === 'dark' ? 'dark bg-gray-950 text-gray-100' : 'bg-gray-50 text-gray-900'}`}>
      {/* Title Bar */}
      <div className="flex items-center justify-between bg-blue-700 text-white px-4 py-2 shadow-md">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold">⚡ PSAT</span>
          <span className="text-sm opacity-75">Power System Analysis Toolbox (ETAP Engine)</span>
        </div>
        <div className="flex items-center gap-3 text-sm font-semibold">
          <span>Active Study:</span>
          <select
            value={activeAnalysis}
            onChange={(e) => {
              setActiveAnalysis(e.target.value as any);
              addOutput(`Selected Study Case: ${e.target.value.replace('-', ' ').toUpperCase()}`);
            }}
            className="bg-blue-800 text-white px-2 py-1 rounded border border-blue-600 focus:outline-none"
          >
            <option value="power-flow">Load Flow (Power Flow)</option>
            <option value="cpf">Continuation Power Flow</option>
            <option value="opf">Optimal Power Flow (OPF)</option>
            <option value="short-circuit">Short Circuit (Faults)</option>
            <option value="transient-stability">Transient Stability</option>
            <option value="small-signal-stability">Small-Signal Stability</option>
          </select>
        </div>
      </div>

      {/* Toolbar */}
      <Toolbar
        onNew={() => {
          setSystem(createDefaultSystem());
          addOutput('Created default power system');
        }}
        onOpen={() => addOutput('Open file dialog')}
        onSave={() => addOutput('Saved power system state')}
        onUndo={undo}
        onRedo={redo}
        onZoomIn={() => zoom(0.1)}
        onZoomOut={() => zoom(-0.1)}
        onFit={() => {
          editorState.zoom = 1;
          editorState.pan = { x: 0, y: 0 };
          addOutput('Zoom reset to Fit');
        }}
        onRunPowerFlow={handleRunAnalysis}
        onRunTimeSim={() => {
          setActiveAnalysis('transient-stability');
          setTimeout(() => handleRunAnalysis(), 50);
        }}
        isProcessing={isProcessing}
      />

      {/* Ribbon */}
      <Ribbon
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onAction={handleAction}
      />

      {/* Center Tab Bar */}
      <div className="flex bg-gray-100 border-b border-gray-300 px-4 py-1">
        <button
          onClick={() => setActiveCenterTab('canvas')}
          className={`px-3 py-1 text-xs font-bold rounded-t mr-1 border-t border-x transition-colors ${
            activeCenterTab === 'canvas' ? 'bg-white text-blue-700 border-gray-300 font-extrabold' : 'bg-gray-200 text-gray-600 border-transparent hover:bg-gray-300'
          }`}
        >
          Single Line Diagram (Canvas)
        </button>
        <button
          onClick={() => setActiveCenterTab('charts')}
          className={`px-3 py-1 text-xs font-bold rounded-t mr-1 border-t border-x transition-colors ${
            activeCenterTab === 'charts' ? 'bg-white text-blue-700 border-gray-300 font-extrabold' : 'bg-gray-200 text-gray-600 border-transparent hover:bg-gray-300'
          }`}
        >
          Analysis Charts
        </button>
        <button
          onClick={() => setActiveCenterTab('reports')}
          className={`px-3 py-1 text-xs font-bold rounded-t border-t border-x transition-colors ${
            activeCenterTab === 'reports' ? 'bg-white text-blue-700 border-gray-300 font-extrabold' : 'bg-gray-200 text-gray-600 border-transparent hover:bg-gray-300'
          }`}
        >
          Detailed Tabular Reports
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        {!sidebarCollapsed && (
          <Sidebar
            system={system}
            onAddBus={handleAddBusFromSidebar}
            onAddLine={() => {
              setMode('add-line');
              addOutput('Mode: Click start bus and end bus on Canvas to add a Line');
            }}
            onAddTransformer={() => {
              setMode('add-transformer');
              addOutput('Mode: Click start bus and end bus on Canvas to add a Transformer');
            }}
            onAddGenerator={() => {
              setMode('add-generator');
              addOutput('Mode: Click a bus on Canvas to attach a Generator');
            }}
            onAddLoad={() => {
              setMode('add-load');
              addOutput('Mode: Click a bus on Canvas to attach a Load');
            }}
            onAddShunt={() => {
              setMode('add-shunt');
              addOutput('Mode: Click a bus on Canvas to attach a Shunt');
            }}
            onCollapse={() => setSidebarCollapsed(true)}
          />
        )}
        
        {sidebarCollapsed && (
          <button
            onClick={() => setSidebarCollapsed(false)}
            className="absolute left-0 top-1/2 bg-gray-200 px-1 py-4 rounded-r-lg shadow-md z-10"
          >
            ▶
          </button>
        )}

        {/* Canvas / Charts / Reports Tabbed Area */}
        <div className="flex-1 flex flex-col overflow-hidden relative">
          <div className="flex-1 flex flex-col bg-white overflow-hidden relative">
            {activeCenterTab === 'canvas' && (
              <Canvas
                system={system}
                selectedBus={selectedBus}
                selectedLine={selectedLine}
                onSelectBus={(busId) => select(busId ? 'bus' : null, busId)}
                onSelectLine={(lineId) => select(lineId ? 'line' : null, lineId)}
                onUpdateBusPosition={handleUpdateBusPosition}
                powerFlowResults={powerFlowResults}
                mode={editorState.mode}
                onAddBus={(x, y, type) => addBus(x, y, type)}
                onAddGenerator={(busId) => addGenerator(busId)}
                onAddLoad={(busId) => addLoad(busId)}
                onAddShunt={(busId) => addShunt(busId)}
                onAddLine={(from, to) => addLine(from, to)}
                onAddTransformer={(from, to) => addTransformer(from, to)}
                onCancelMode={() => setMode('select')}
                addOutput={addOutput}
              />
            )}

            {activeCenterTab === 'charts' && (
              <AnalysisCharts
                activeAnalysis={activeAnalysis}
                cpfResults={cpfResults}
                timeseriesResults={timeseriesResults}
                stabilityResults={stabilityResults}
              />
            )}

            {activeCenterTab === 'reports' && (
              <TabularReports
                activeAnalysis={activeAnalysis}
                system={system}
                powerFlowResults={powerFlowResults}
                cpfResults={cpfResults}
                opfResults={opfResults}
                faultResults={faultResults}
                timeseriesResults={timeseriesResults}
                stabilityResults={stabilityResults}
              />
            )}
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
            onUpdateBus={(bus) => updateBus(bus.id, bus)}
            onUpdateLine={(line) => updateLine(line.id, line)}
            onCollapse={() => setPropertiesPanelCollapsed(true)}
          />
        )}
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between bg-gray-200 border-t border-gray-300 px-4 py-1 text-xs text-gray-600">
        <div className="flex items-center gap-4">
          <span>Buses: {system.buses.length}</span>
          <span>Lines: {system.lines.length}</span>
          <span>Transformers: {system.transformers?.length || 0}</span>
          <span>Loads: {system.loads.length}</span>
          <span>Generators: {system.generators.length}</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Mode: <span className="font-bold text-blue-600 uppercase">{editorState.mode}</span></span>
          <span>Base: {settings.basePower} MVA</span>
          <span>Freq: {settings.baseFrequency} Hz</span>
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
        <SettingsDialog
          settings={settings}
          onSave={setSettings}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
}