'use client';

import { useState } from 'react';
import { PowerSystem, PowerFlowResult } from '@/types';
import { downloadReport, generateReport } from '@/lib/reports';

interface TabularReportsProps {
  activeAnalysis: string;
  system: PowerSystem;
  powerFlowResults: PowerFlowResult | null;
  cpfResults: any;
  opfResults: any;
  faultResults: any;
  timeseriesResults: any;
  stabilityResults: any;
}

export default function TabularReports({
  activeAnalysis,
  system,
  powerFlowResults,
  cpfResults,
  opfResults,
  faultResults,
  timeseriesResults,
  stabilityResults
}: TabularReportsProps) {
  const [reportTab, setReportTab] = useState<'buses' | 'branches' | 'general'>('general');

  // Helper to trigger download
  const handleDownload = (format: 'html' | 'csv' | 'json') => {
    const title = `${activeAnalysis.replace('-', ' ').toUpperCase()} Report`;
    const reportData: any = {
      title,
      date: new Date(),
      system,
      notes: `Report generated automatically on PSAT Web interface.`
    };

    if (powerFlowResults) reportData.powerFlow = powerFlowResults;
    if (cpfResults) reportData.cpf = cpfResults;
    if (opfResults) reportData.opf = opfResults;
    if (faultResults) reportData.faultStudy = faultResults;
    if (stabilityResults) reportData.stability = stabilityResults;

    const sections = generateReport(reportData);
    downloadReport(sections, title, format);
  };

  return (
    <div className="flex-1 flex flex-col p-4 bg-gray-50 h-full overflow-hidden">
      {/* Header and Download buttons */}
      <div className="flex items-center justify-between mb-3 bg-white p-3 border border-gray-300 rounded-lg shadow-sm">
        <div className="flex items-center gap-2">
          <span className="font-bold text-sm text-gray-800">Study Report:</span>
          <span className="text-sm px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-semibold capitalize">
            {activeAnalysis.replace('-', ' ')}
          </span>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleDownload('html')}
            className="px-3 py-1 bg-blue-600 text-white rounded text-xs font-semibold hover:bg-blue-700 transition-colors"
          >
            Download HTML
          </button>
          <button
            onClick={() => handleDownload('csv')}
            className="px-3 py-1 bg-green-600 text-white rounded text-xs font-semibold hover:bg-green-700 transition-colors"
          >
            Download CSV
          </button>
          <button
            onClick={() => handleDownload('json')}
            className="px-3 py-1 bg-gray-600 text-white rounded text-xs font-semibold hover:bg-gray-700 transition-colors"
          >
            Download JSON
          </button>
        </div>
      </div>

      {/* Report Navigation Tabs */}
      <div className="flex bg-gray-200 border border-gray-300 border-b-0 rounded-t-lg">
        <button
          onClick={() => setReportTab('general')}
          className={`px-4 py-2 text-xs font-bold transition-colors ${
            reportTab === 'general' ? 'bg-white border-b-2 border-blue-500 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          System Summary
        </button>
        <button
          onClick={() => setReportTab('buses')}
          className={`px-4 py-2 text-xs font-bold transition-colors ${
            reportTab === 'buses' ? 'bg-white border-b-2 border-blue-500 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          Bus Voltages & Injection
        </button>
        <button
          onClick={() => setReportTab('branches')}
          className={`px-4 py-2 text-xs font-bold transition-colors ${
            reportTab === 'branches' ? 'bg-white border-b-2 border-blue-500 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          Branch Flows & Loading
        </button>
      </div>

      {/* Report Content */}
      <div className="flex-1 bg-white border border-gray-300 rounded-b-lg p-4 overflow-y-auto shadow-sm">
        {reportTab === 'general' && (
          <div className="space-y-4">
            <h3 className="font-bold text-sm text-gray-700 border-b pb-1">System Infrastructure Summary</h3>
            <div className="grid grid-cols-2 gap-4 max-w-lg">
              <div className="text-sm text-gray-600">Base Power (MVA):</div>
              <div className="text-sm font-mono font-bold text-gray-800">{system.baseMVA || 100} MVA</div>

              <div className="text-sm text-gray-600">Base Frequency:</div>
              <div className="text-sm font-mono font-bold text-gray-800">{system.baseFreq || 60} Hz</div>

              <div className="text-sm text-gray-600">Total Buses:</div>
              <div className="text-sm font-mono font-bold text-gray-800">{system.buses.length}</div>

              <div className="text-sm text-gray-600">Total Transmission Lines:</div>
              <div className="text-sm font-mono font-bold text-gray-800">{system.lines.length}</div>

              <div className="text-sm text-gray-600">Transformers Installed:</div>
              <div className="text-sm font-mono font-bold text-gray-800">{system.transformers?.length || 0}</div>

              <div className="text-sm text-gray-600">Generators Active:</div>
              <div className="text-sm font-mono font-bold text-gray-800">
                {system.generators.filter(g => g.active).length} / {system.generators.length}
              </div>

              <div className="text-sm text-gray-600">Loads Connected:</div>
              <div className="text-sm font-mono font-bold text-gray-800">
                {system.loads.filter(l => l.active).length} / {system.loads.length}
              </div>
            </div>

            {/* Render results metadata if available */}
            {powerFlowResults && (
              <div className="mt-6 pt-4 border-t border-gray-200">
                <h4 className="font-bold text-xs text-gray-700 uppercase mb-2">Calculation Metrics</h4>
                <div className="grid grid-cols-2 gap-2 max-w-lg font-mono text-xs">
                  <div>Solver Method:</div>
                  <div className="font-bold">{powerFlowResults.method}</div>
                  <div>Convergence status:</div>
                  <div className={powerFlowResults.converged ? 'text-green-600 font-bold' : 'text-red-600 font-bold'}>
                    {powerFlowResults.converged ? 'CONVERGED' : 'FAILED'}
                  </div>
                  <div>Iterations:</div>
                  <div className="font-bold">{powerFlowResults.iterations}</div>
                  <div>Max Mismatch:</div>
                  <div className="font-bold">{powerFlowResults.maxMismatch.toExponential(4)}</div>
                  <div>Total Active Losses:</div>
                  <div className="font-bold">{(powerFlowResults.losses?.real || 0).toFixed(4)} MW</div>
                </div>
              </div>
            )}
          </div>
        )}

        {reportTab === 'buses' && (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-xs text-gray-600">
              <thead className="bg-gray-100 uppercase text-gray-700 font-bold border-b border-gray-300">
                <tr>
                  <th className="px-4 py-2.5">Bus Name</th>
                  <th className="px-4 py-2.5">Type</th>
                  <th className="px-4 py-2.5">Voltage (pu)</th>
                  <th className="px-4 py-2.5">Angle (deg)</th>
                  <th className="px-4 py-2.5">Gen P (MW)</th>
                  <th className="px-4 py-2.5">Gen Q (MVAR)</th>
                  <th className="px-4 py-2.5">Load P (MW)</th>
                  <th className="px-4 py-2.5">Load Q (MVAR)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {system.buses.map((bus, idx) => {
                  const pfRes = powerFlowResults?.busResults?.find(r => r.bus === bus.id);
                  const voltage = pfRes ? pfRes.v : bus.voltage;
                  const angle = pfRes ? pfRes.angle : bus.angle;

                  // Find generator or load attached to this bus
                  const busGens = system.generators.filter(g => g.bus === bus.id && g.active);
                  const busLoads = system.loads.filter(l => l.bus === bus.id && l.active);

                  const genP = busGens.reduce((sum, g) => sum + g.pg, 0) * (system.baseMVA || 100);
                  const genQ = busGens.reduce((sum, g) => sum + g.qg, 0) * (system.baseMVA || 100);
                  const loadP = busLoads.reduce((sum, l) => sum + l.pl, 0) * (system.baseMVA || 100);
                  const loadQ = busLoads.reduce((sum, l) => sum + l.ql, 0) * (system.baseMVA || 100);

                  return (
                    <tr key={bus.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 font-bold text-gray-900">{bus.name}</td>
                      <td className="px-4 py-2 uppercase font-medium">{bus.type}</td>
                      <td className={`px-4 py-2 font-mono font-bold ${voltage < bus.vmin || voltage > bus.vmax ? 'text-red-600' : 'text-gray-900'}`}>
                        {voltage.toFixed(4)}
                      </td>
                      <td className="px-4 py-2 font-mono">{angle.toFixed(2)}°</td>
                      <td className="px-4 py-2 font-mono">{genP.toFixed(2)}</td>
                      <td className="px-4 py-2 font-mono">{genQ.toFixed(2)}</td>
                      <td className="px-4 py-2 font-mono">{loadP.toFixed(2)}</td>
                      <td className="px-4 py-2 font-mono">{loadQ.toFixed(2)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {reportTab === 'branches' && (
          <div className="space-y-6">
            <div>
              <h4 className="font-bold text-xs uppercase text-gray-700 mb-2 border-b pb-1">Transmission Lines</h4>
              <div className="overflow-x-auto">
                <table className="min-w-full text-left text-xs text-gray-600">
                  <thead className="bg-gray-100 uppercase text-gray-700 font-bold border-b border-gray-300">
                    <tr>
                      <th className="px-4 py-2">ID</th>
                      <th className="px-4 py-2">From</th>
                      <th className="px-4 py-2">To</th>
                      <th className="px-4 py-2">P Flow (MW)</th>
                      <th className="px-4 py-2">Q Flow (MVAR)</th>
                      <th className="px-4 py-2">P Loss (MW)</th>
                      <th className="px-4 py-2">Rating (MVA)</th>
                      <th className="px-4 py-2">Loading (%)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {system.lines.map(line => {
                      const pfRes = powerFlowResults?.lineResults?.find(r => r.line === line.id);
                      const pFlow = pfRes ? pfRes.pFrom : 0;
                      const qFlow = pfRes ? pfRes.qFrom : 0;
                      const pLoss = pfRes ? pfRes.ploss : 0;
                      const loading = pfRes ? pfRes.loading : 0;

                      return (
                        <tr key={line.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 font-bold text-gray-900">{line.id}</td>
                          <td className="px-4 py-2">{line.fromBus}</td>
                          <td className="px-4 py-2">{line.toBus}</td>
                          <td className="px-4 py-2 font-mono">{pFlow.toFixed(2)}</td>
                          <td className="px-4 py-2 font-mono">{qFlow.toFixed(2)}</td>
                          <td className="px-4 py-2 font-mono text-red-500">{pLoss.toFixed(3)}</td>
                          <td className="px-4 py-2 font-mono">{line.rating}</td>
                          <td className={`px-4 py-2 font-mono font-bold ${loading > 80 ? 'text-red-600' : 'text-green-600'}`}>
                            {loading.toFixed(1)}%
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {system.transformers && system.transformers.length > 0 && (
              <div>
                <h4 className="font-bold text-xs uppercase text-gray-700 mb-2 border-b pb-1">Transformers</h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full text-left text-xs text-gray-600">
                    <thead className="bg-gray-100 uppercase text-gray-700 font-bold border-b border-gray-300">
                      <tr>
                        <th className="px-4 py-2">ID</th>
                        <th className="px-4 py-2">From Bus</th>
                        <th className="px-4 py-2">To Bus</th>
                        <th className="px-4 py-2">Tap Ratio</th>
                        <th className="px-4 py-2">Phase Shift</th>
                        <th className="px-4 py-2">Reactance (X)</th>
                        <th className="px-4 py-2">Rating (MVA)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {system.transformers.map(txf => (
                        <tr key={txf.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 font-bold text-gray-900">{txf.id}</td>
                          <td className="px-4 py-2">{txf.fromBus}</td>
                          <td className="px-4 py-2">{txf.toBus}</td>
                          <td className="px-4 py-2 font-mono">{txf.tap.toFixed(3)}</td>
                          <td className="px-4 py-2 font-mono">{txf.shift.toFixed(1)}°</td>
                          <td className="px-4 py-2 font-mono">{txf.reactance.toFixed(4)}</td>
                          <td className="px-4 py-2 font-mono">{txf.rating}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
