'use client';

import { useState, useCallback } from 'react';
import dynamic from 'next/dynamic';
import Ribbon from '@/components/Ribbon';
import Toolbar from '@/components/Toolbar';
import Sidebar from '@/components/Sidebar';
import PropertiesPanel from '@/components/PropertiesPanel';
import OutputWindow from '@/components/OutputWindow';
import SettingsDialog from '@/components/SettingsDialog';
import { PowerSystem, PowerFlowResult, CPFResult, EigenvalueResult, SimulationResult, OPFResult, SimulationParams, Settings, defaultSettings } from '@/types';
import { createDefaultSystem, PowerFlowSolver } from '@/lib/powerflow';
import { CPFSolver } from '@/lib/cpf';
import { EigenvalueAnalyzer } from '@/lib/eigen';
import { TimeDomainSimulator } from '@/lib/timedomain';
import { OPFSolver } from '@/lib/opf';
import { serializeSystem, deserializeSystem, saveToFile, loadFromFile, exportToMatpower, exportToRaw } from '@/lib/io';
import { ReportGenerator } from '@/lib/report';
import '@/app/globals.css';

const Canvas = dynamic(() => import('@/components/Canvas'), { ssr: false });

export default function Home() {
  const [system, setSystem] = useState<PowerSystem>(createDefaultSystem());
  const [selectedBus, setSelectedBus] = useState<string | null>(null);
  const [selectedLine, setSelectedLine] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('home');
  const [powerFlowResults, setPowerFlowResults] = useState<PowerFlowResult | null>(null);
  const [cpfResult, setCpfResult] = useState<CPFResult | null>(null);
  const [eigenResult, setEigenResult] = useState<EigenvalueResult | null>(null);
  const [simResult, setSimResult] = useState<SimulationResult | null>(null);
  const [opfResult, setOpfResult] = useState<OPFResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showCpf, setShowCpf] = useState(false);
  const [showEigen, setShowEigen] = useState(false);
  const [showSim, setShowSim] = useState(false);
  const [showOpf, setShowOpf] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const [reportContent, setReportContent] = useState('');
  const [output, setOutput] = useState<string[]>([]);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [propertiesPanelCollapsed, setPropertiesPanelCollapsed] = useState(false);
  const [simParams, setSimParams] = useState<SimulationParams>({ tStart: 0, tEnd: 20, stepSize: 0.01, faultLocation: '', faultTime: 1, faultDuration: 0.1 });

  const addOutput = (message: string) => {
    setOutput(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  const handleAction = useCallback((action: string) => {
    switch (action) {
      case 'power-flow': handleRunPowerFlow(); break;
      case 'cpf': setShowCpf(true); break;
      case 'opf': setShowOpf(true); break;
      case 'time-sim': setShowSim(true); break;
      case 'eigenvalue': setShowEigen(true); break;
      case 'modal': addOutput('Modal analysis - use Eigenvalue tool'); break;
      case 'settings': setShowSettings(true); break;
      case 'open': handleOpen(); break;
      case 'save': handleSave(); break;
      case 'export': handleExport(); break;
      case 'report': generateReport(); break;
      case 'summary': generateSummary(); break;
      default: addOutput(`Action: ${action}`);
    }
  }, [system, powerFlowResults, cpfResult, eigenResult, simResult, opfResult]);

  const handleRunPowerFlow = async () => {
    setIsProcessing(true);
    addOutput('Starting Newton-Raphson Power Flow...');
    await new Promise(r => setTimeout(r, 100));
    try {
      const solver = new PowerFlowSolver(system);
      const results = solver.solve('nr');
      setPowerFlowResults(results);
      addOutput(`Power Flow ${results.converged ? 'CONVERGED' : 'FAILED'}`);
      addOutput(`  Iterations: ${results.iterations}, Max Mismatch: ${results.maxMismatch.toExponential(3)}`);
      addOutput(`  Total Losses: ${results.losses.real.toFixed(6)} pu, ${results.losses.reactive.toFixed(6)} pu`);
      results.busResults.forEach(br => {
        addOutput(`  Bus ${br.id}: V=${br.voltage.toFixed(4)} pu, Ang=${br.angle.toFixed(2)} deg`);
      });
    } catch (error) {
      addOutput(`Error: ${error}`);
    }
    setIsProcessing(false);
  };

  const handleRunCPF = async () => {
    setIsProcessing(true);
    addOutput('Starting Continuation Power Flow...');
    await new Promise(r => setTimeout(r, 100));
    try {
      const solver = new CPFSolver(system);
      const result = solver.solve({ showProgress: true });
      setCpfResult(result);
      addOutput(`CPF ${result.converged ? 'CONVERGED' : 'stopped'}`);
      addOutput(`  Critical Lambda: ${result.criticalLambda.toFixed(4)}`);
      addOutput(`  Critical Bus: ${result.criticalBus}`);
      addOutput(`  Points: ${result.points.length}`);
    } catch (error) {
      addOutput(`CPF Error: ${error}`);
    }
    setShowCpf(false);
    setIsProcessing(false);
  };

  const handleRunEigen = async () => {
    setIsProcessing(true);
    addOutput('Starting Eigenvalue Analysis...');
    await new Promise(r => setTimeout(r, 100));
    try {
      const analyzer = new EigenvalueAnalyzer(system);
      const result = analyzer.analyze(powerFlowResults || undefined);
      setEigenResult(result);
      const stable = result.eigenvalues.filter(e => e.real < 0).length;
      const unstable = result.eigenvalues.filter(e => e.real > 1e-6).length;
      addOutput(`Eigenvalue Analysis complete: ${result.eigenvalues.length} eigenvalues`);
      addOutput(`  Stable: ${stable}, Unstable: ${unstable}`);
      addOutput(`  Frequency range: ${Math.min(...result.frequencies.filter(f => f > 0)).toFixed(4) || 0} - ${Math.max(...result.frequencies).toFixed(4)} Hz`);
    } catch (error) {
      addOutput(`Eigen Error: ${error}`);
    }
    setShowEigen(false);
    setIsProcessing(false);
  };

  const handleRunSim = async () => {
    setIsProcessing(true);
    addOutput('Starting Time Domain Simulation...');
    await new Promise(r => setTimeout(r, 100));
    try {
      const simulator = new TimeDomainSimulator(system);
      const result = simulator.simulate(simParams);
      setSimResult(result);
      addOutput(`Time Simulation complete: ${result.time.length} time points`);
      addOutput(`  Duration: ${result.time[0].toFixed(2)}s to ${result.time[result.time.length - 1].toFixed(2)}s`);
    } catch (error) {
      addOutput(`Sim Error: ${error}`);
    }
    setShowSim(false);
    setIsProcessing(false);
  };

  const handleRunOPF = async () => {
    setIsProcessing(true);
    addOutput('Starting Optimal Power Flow...');
    await new Promise(r => setTimeout(r, 100));
    try {
      const solver = new OPFSolver(system);
      const result = solver.solve({ objective: 'min-cost' });
      setOpfResult(result);
      addOutput(`OPF ${result.converged ? 'CONVERGED' : 'FAILED'}`);
      addOutput(`  Iterations: ${result.iterations}, Objective: ${result.objectiveValue.toFixed(4)}`);
    } catch (error) {
      addOutput(`OPF Error: ${error}`);
    }
    setShowOpf(false);
    setIsProcessing(false);
  };

  const handleOpen = async () => {
    try {
      const content = await loadFromFile();
      const loaded = deserializeSystem(content);
      if (loaded) {
        setSystem(loaded);
        setPowerFlowResults(null); setCpfResult(null); setEigenResult(null); setSimResult(null); setOpfResult(null);
        addOutput(`Loaded system: ${loaded.buses.length} buses, ${loaded.lines.length} lines`);
      } else {
        addOutput('Failed to parse system file');
      }
    } catch (e: any) {
      addOutput(`Open cancelled or error: ${e.message}`);
    }
  };

  const handleSave = () => {
    const json = serializeSystem(system);
    saveToFile(json, `psat_system_${Date.now()}.json`);
    addOutput('System saved');
  };

  const handleExport = () => {
    const matpower = exportToMatpower(system);
    saveToFile(matpower, `psat_export_${Date.now()}.m`, 'text/plain');
    addOutput('System exported to Matpower format');
  };

  const generateReport = () => {
    if (powerFlowResults) {
      const report = ReportGenerator.powerFlowReport(system, powerFlowResults);
      setReportContent(report);
      setShowReport(true);
      addOutput('Report generated');
    } else {
      addOutput('Run Power Flow first to generate report');
    }
  };

  const generateSummary = () => {
    const lines: string[] = [];
    lines.push('='.repeat(60));
    lines.push('  PSAT SYSTEM SUMMARY');
    lines.push('='.repeat(60));
    lines.push(`  Buses: ${system.buses.length}`);
    system.buses.forEach(b => lines.push(`    ${b.id}: ${b.name} (${b.type.toUpperCase()}) V=${b.voltage} pu`));
    lines.push(`  Lines: ${system.lines.length}`);
    system.lines.forEach(l => lines.push(`    ${l.id}: ${l.fromBus}->${l.toBus} R=${l.resistance} X=${l.reactance}`));
    lines.push(`  Generators: ${system.generators.length}`);
    lines.push(`  Loads: ${system.loads.length}`);
    lines.push(`  Transformers: ${system.transformers.length}`);
    lines.push(`  Shunts: ${system.shunts.length}`);
    lines.push(`  Areas: ${system.areas.length}`);
    if (powerFlowResults) lines.push(`  Power Flow: ${powerFlowResults.converged ? 'Converged' : 'Not converged'}, ${powerFlowResults.iterations} iterations`);
    lines.push('='.repeat(60));
    setReportContent(lines.join('\n'));
    setShowReport(true);
    addOutput('Summary generated');
  };

  const handleUpdateBusPosition = (busId: string, x: number, y: number) => {
    setSystem(prev => ({ ...prev, buses: prev.buses.map(b => b.id === busId ? { ...b, x, y } : b) }));
  };

  const handleAddBus = (type: 'slack' | 'pv' | 'pq') => {
    const newId = `bus_${Date.now()}`;
    setSystem(prev => ({
      ...prev,
      buses: [...prev.buses, {
        id: newId, name: `Bus ${prev.buses.length + 1}`, type,
        voltage: type === 'slack' ? 1.0 : type === 'pv' ? 1.05 : 1.0,
        angle: 0, vmin: 0.9, vmax: 1.1, area: 1, region: 1,
        x: Math.random() * 5 - 2.5, y: Math.random() * 5 - 2.5, active: true
      }]
    }));
    addOutput(`Added ${type} bus: ${newId}`);
  };

  const handleAddLine = () => {
    if (system.buses.length < 2) { addOutput('Need at least 2 buses'); return; }
    const newId = `line_${Date.now()}`;
    setSystem(prev => ({
      ...prev,
      lines: [...prev.lines, {
        id: newId, fromBus: prev.buses[0].id, toBus: prev.buses[1].id,
        resistance: 0.02, reactance: 0.04, susceptance: 0, rating: 100, active: true
      }]
    }));
    addOutput(`Added line: ${newId}`);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Title Bar */}
      <div className="flex items-center justify-between bg-blue-700 text-white px-4 py-2 shadow-md">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold">PSAT</span>
          <span className="text-sm opacity-75">Power System Analysis Toolbox</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="cursor-pointer hover:underline" onClick={handleOpen}>File</span>
          <span className="cursor-pointer hover:underline" onClick={handleSave}>Save</span>
          <span className="cursor-pointer hover:underline" onClick={handleExport}>Export</span>
          <span className="cursor-pointer hover:underline" onClick={() => setShowSettings(true)}>Settings</span>
        </div>
      </div>

      <Toolbar
        onNew={() => { setSystem(createDefaultSystem()); setPowerFlowResults(null); setCpfResult(null); setEigenResult(null); setSimResult(null); setOpfResult(null); addOutput('New system created'); }}
        onOpen={handleOpen} onSave={handleSave}
        onUndo={() => addOutput('Undo')} onRedo={() => addOutput('Redo')}
        onZoomIn={() => {}} onZoomOut={() => {}} onFit={() => {}}
        onRunPowerFlow={handleRunPowerFlow}
        onRunTimeSim={() => setShowSim(true)}
        isProcessing={isProcessing}
      />

      <Ribbon activeTab={activeTab} onTabChange={setActiveTab} onAction={handleAction} />

      <div className="flex flex-1 overflow-hidden">
        {!sidebarCollapsed ? (
          <Sidebar system={system} onAddBus={handleAddBus} onAddLine={handleAddLine} onCollapse={() => setSidebarCollapsed(true)} />
        ) : (
          <button onClick={() => setSidebarCollapsed(false)} className="bg-gray-200 px-1 py-4 rounded-r-lg shadow-md self-center">▶</button>
        )}

        <div className="flex-1 flex flex-col">
          <div className="flex-1 bg-white border border-gray-300 relative">
            <Canvas system={system} selectedBus={selectedBus} selectedLine={selectedLine}
              onSelectBus={setSelectedBus} onSelectLine={setSelectedLine}
              onUpdateBusPosition={handleUpdateBusPosition} powerFlowResults={powerFlowResults} />
          </div>
          <OutputWindow messages={output} onClear={() => setOutput([])} />
        </div>

        {!propertiesPanelCollapsed ? (
          <PropertiesPanel system={system} selectedBus={selectedBus} selectedLine={selectedLine}
            powerFlowResults={powerFlowResults} onUpdateBus={() => {}} onUpdateLine={() => {}}
            onCollapse={() => setPropertiesPanelCollapsed(true)} />
        ) : (
          <button onClick={() => setPropertiesPanelCollapsed(false)} className="bg-gray-200 px-1 py-4 rounded-l-lg shadow-md self-center">◀</button>
        )}
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between bg-gray-200 border-t border-gray-300 px-4 py-1 text-xs text-gray-600">
        <div className="flex items-center gap-4">
          <span>Buses: {system.buses.length}</span>
          <span>Lines: {system.lines.length}</span>
          <span>TX: {system.transformers.length}</span>
          <span>Loads: {system.loads.length}</span>
          <span>Gens: {system.generators.length}</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Base: 100 MVA</span>
          <span>Freq: 50 Hz</span>
          {powerFlowResults && (
            <span className={powerFlowResults.converged ? 'text-green-600' : 'text-red-600'}>
              {powerFlowResults.converged ? 'Converged' : 'Failed'} ({powerFlowResults.iterations} iter)
            </span>
          )}
        </div>
      </div>

      {showSettings && <SettingsDialog onClose={() => setShowSettings(false)} />}

      {/* CPF Dialog */}
      {showCpf && (
        <Modal title="Continuation Power Flow" onClose={() => setShowCpf(false)}>
          <p className="text-sm text-gray-600 mb-4">Compute PV curves and voltage stability margin by progressively increasing system load.</p>
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowCpf(false)} className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
            <button onClick={handleRunCPF} disabled={isProcessing} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">Run CPF</button>
          </div>
        </Modal>
      )}

      {/* Eigenvalue Dialog */}
      {showEigen && (
        <Modal title="Eigenvalue Analysis" onClose={() => setShowEigen(false)}>
          <p className="text-sm text-gray-600 mb-4">Compute eigenvalues of the power flow Jacobian for small-signal stability assessment.</p>
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowEigen(false)} className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
            <button onClick={handleRunEigen} disabled={isProcessing} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">Run Analysis</button>
          </div>
        </Modal>
      )}

      {/* Time Simulation Dialog */}
      {showSim && (
        <Modal title="Time Domain Simulation" onClose={() => setShowSim(false)}>
          <div className="space-y-3 mb-4">
            <div className="flex justify-between items-center">
              <label className="text-sm text-gray-600">Start Time (s)</label>
              <input type="number" value={simParams.tStart} onChange={e => setSimParams({...simParams, tStart: parseFloat(e.target.value) || 0})} className="w-24 px-2 py-1 border rounded text-sm" />
            </div>
            <div className="flex justify-between items-center">
              <label className="text-sm text-gray-600">End Time (s)</label>
              <input type="number" value={simParams.tEnd} onChange={e => setSimParams({...simParams, tEnd: parseFloat(e.target.value) || 20})} className="w-24 px-2 py-1 border rounded text-sm" />
            </div>
            <div className="flex justify-between items-center">
              <label className="text-sm text-gray-600">Step Size (s)</label>
              <input type="number" value={simParams.stepSize} onChange={e => setSimParams({...simParams, stepSize: parseFloat(e.target.value) || 0.01})} className="w-24 px-2 py-1 border rounded text-sm" step="0.001" />
            </div>
            <div className="flex justify-between items-center">
              <label className="text-sm text-gray-600">Fault Time (s)</label>
              <input type="number" value={simParams.faultTime} onChange={e => setSimParams({...simParams, faultTime: parseFloat(e.target.value) || 1})} className="w-24 px-2 py-1 border rounded text-sm" step="0.1" />
            </div>
            <div className="flex justify-between items-center">
              <label className="text-sm text-gray-600">Fault Duration (s)</label>
              <input type="number" value={simParams.faultDuration} onChange={e => setSimParams({...simParams, faultDuration: parseFloat(e.target.value) || 0.1})} className="w-24 px-2 py-1 border rounded text-sm" step="0.05" />
            </div>
          </div>
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowSim(false)} className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
            <button onClick={handleRunSim} disabled={isProcessing} className="px-4 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">Run Simulation</button>
          </div>
        </Modal>
      )}

      {/* OPF Dialog */}
      {showOpf && (
        <Modal title="Optimal Power Flow" onClose={() => setShowOpf(false)}>
          <p className="text-sm text-gray-600 mb-4">Solve optimal power flow to minimize generation cost while satisfying network constraints.</p>
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowOpf(false)} className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
            <button onClick={handleRunOPF} disabled={isProcessing} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">Run OPF</button>
          </div>
        </Modal>
      )}

      {/* Report Dialog */}
      {showReport && (
        <Modal title="PSAT Report" onClose={() => setShowReport(false)} wide>
          <pre className="text-xs font-mono bg-gray-900 text-gray-300 p-4 rounded overflow-auto max-h-96">{reportContent}</pre>
          <div className="flex justify-end gap-2 mt-4">
            <button onClick={() => { saveToFile(reportContent, `psat_report_${Date.now()}.txt`, 'text/plain'); addOutput('Report saved'); }} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">Save Report</button>
            <button onClick={() => setShowReport(false)} className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">Close</button>
          </div>
        </Modal>
      )}
    </div>
  );
}

function Modal({ title, children, onClose, wide = false }: { title: string; children: React.ReactNode; onClose: () => void; wide?: boolean }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`bg-white rounded-lg shadow-xl ${wide ? 'w-[700px]' : 'w-[450px]'} max-h-[80vh] overflow-hidden`}>
        <div className="flex items-center justify-between px-4 py-3 bg-blue-600 text-white">
          <h2 className="text-lg font-medium">{title}</h2>
          <button onClick={onClose} className="text-2xl hover:opacity-80">x</button>
        </div>
        <div className="p-4 overflow-y-auto">{children}</div>
      </div>
    </div>
  );
}
