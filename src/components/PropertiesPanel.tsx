'use client';

import { useState } from 'react';
import { PowerSystem, PowerFlowResult } from '@/types';

interface PropertiesPanelProps {
  system: PowerSystem;
  selectedBus: string | null;
  selectedLine: string | null;
  powerFlowResults: PowerFlowResult | null;
  onUpdateBus: (bus: any) => void;
  onUpdateLine: (line: any) => void;
  onCollapse: () => void;
}

export default function PropertiesPanel({
  system,
  selectedBus,
  selectedLine,
  powerFlowResults,
  onUpdateBus,
  onUpdateLine,
  onCollapse
}: PropertiesPanelProps) {
  const [activeTab, setActiveTab] = useState<'bus' | 'line'>('bus');

  const selectedBusData = system.buses.find(b => b.id === selectedBus);
  const selectedLineData = system.lines.find(l => l.id === selectedLine);
  
  const busResult = selectedBus && powerFlowResults?.busResults 
    ? powerFlowResults.busResults.find(r => r.id === selectedBus)
    : null;
  
  const lineResult = selectedLine && powerFlowResults?.lineResults
    ? powerFlowResults.lineResults.find(r => r.id === selectedLine)
    : null;

  return (
    <div className="w-72 bg-gray-100 border-l border-gray-300 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-gray-200 border-b border-gray-300">
        <span className="font-medium text-sm">Properties</span>
        <button
          onClick={onCollapse}
          className="text-gray-500 hover:text-gray-700 text-lg"
        >
          ×
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-300">
        <button
          onClick={() => setActiveTab('bus')}
          className={`flex-1 px-3 py-2 text-sm font-medium ${
            activeTab === 'bus'
              ? 'bg-white border-b-2 border-blue-500'
              : 'bg-gray-50 hover:bg-gray-100'
          }`}
        >
          Bus
        </button>
        <button
          onClick={() => setActiveTab('line')}
          className={`flex-1 px-3 py-2 text-sm font-medium ${
            activeTab === 'line'
              ? 'bg-white border-b-2 border-blue-500'
              : 'bg-gray-50 hover:bg-gray-100'
          }`}
        >
          Line
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-3">
        {activeTab === 'bus' && (
          <div className="space-y-3">
            {selectedBusData ? (
              <>
                <PropertyGroup title="Identification">
                  <PropertyRow label="ID" value={selectedBusData.id} />
                  <PropertyRow label="Name" value={selectedBusData.name} />
                  <PropertyRow label="Type" value={selectedBusData.type.toUpperCase()} />
                </PropertyGroup>

                <PropertyGroup title="Voltage">
                  <PropertyInput 
                    label="Voltage (pu)" 
                    value={selectedBusData.voltage} 
                    onChange={(v) => onUpdateBus({ ...selectedBusData, voltage: v })} 
                  />
                  <PropertyRow label="Angle" value={`${selectedBusData.angle.toFixed(2)}°`} />
                </PropertyGroup>

                <PropertyGroup title="Limits">
                  <PropertyInput 
                    label="Vmin" 
                    value={selectedBusData.vmin} 
                    onChange={(v) => onUpdateBus({ ...selectedBusData, vmin: v })} 
                  />
                  <PropertyInput 
                    label="Vmax" 
                    value={selectedBusData.vmax} 
                    onChange={(v) => onUpdateBus({ ...selectedBusData, vmax: v })} 
                  />
                </PropertyGroup>

                <PropertyGroup title="Location">
                  <PropertyRow label="Area" value={selectedBusData.area.toString()} />
                  <PropertyRow label="Region" value={selectedBusData.region.toString()} />
                  <PropertyRow label="X" value={selectedBusData.x.toFixed(2)} />
                  <PropertyRow label="Y" value={selectedBusData.y.toFixed(2)} />
                </PropertyGroup>

                {busResult && (
                  <PropertyGroup title="Power Flow Results">
                    <PropertyRow label="Voltage" value={`${busResult.voltage.toFixed(4)} pu`} />
                    <PropertyRow label="Angle" value={`${busResult.angle.toFixed(2)}°`} />
                    <PropertyRow label="P Gen" value={`${busResult.pGen.toFixed(4)} MW`} />
                    <PropertyRow label="Q Gen" value={`${busResult.qGen.toFixed(4)} Mvar`} />
                    <PropertyRow label="P Load" value={`${busResult.pLoad.toFixed(4)} MW`} />
                    <PropertyRow label="Q Load" value={`${busResult.qLoad.toFixed(4)} Mvar`} />
                  </PropertyGroup>
                )}
              </>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <p>No bus selected</p>
                <p className="text-xs mt-2">Click on a bus to view its properties</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'line' && (
          <div className="space-y-3">
            {selectedLineData ? (
              <>
                <PropertyGroup title="Identification">
                  <PropertyRow label="ID" value={selectedLineData.id} />
                  <PropertyRow label="From Bus" value={selectedLineData.fromBus} />
                  <PropertyRow label="To Bus" value={selectedLineData.toBus} />
                </PropertyGroup>

                <PropertyGroup title="Impedance">
                  <PropertyInput 
                    label="R (pu)" 
                    value={selectedLineData.resistance} 
                    onChange={(v) => onUpdateLine({ ...selectedLineData, resistance: v })} 
                  />
                  <PropertyInput 
                    label="X (pu)" 
                    value={selectedLineData.reactance} 
                    onChange={(v) => onUpdateLine({ ...selectedLineData, reactance: v })} 
                  />
                  <PropertyInput 
                    label="B (pu)" 
                    value={selectedLineData.susceptance} 
                    onChange={(v) => onUpdateLine({ ...selectedLineData, susceptance: v })} 
                  />
                </PropertyGroup>

                <PropertyGroup title="Rating">
                  <PropertyInput 
                    label="Rate (MVA)" 
                    value={selectedLineData.rating} 
                    onChange={(v) => onUpdateLine({ ...selectedLineData, rating: v })} 
                  />
                </PropertyGroup>

                {lineResult && (
                  <PropertyGroup title="Power Flow Results">
                    <PropertyRow label="P From" value={`${lineResult.pFrom.toFixed(4)} MW`} />
                    <PropertyRow label="Q From" value={`${lineResult.qFrom.toFixed(4)} Mvar`} />
                    <PropertyRow label="P To" value={`${lineResult.pTo.toFixed(4)} MW`} />
                    <PropertyRow label="Q To" value={`${lineResult.qTo.toFixed(4)} Mvar`} />
                    <PropertyRow 
                      label="Loading" 
                      value={`${lineResult.loading.toFixed(1)}%`}
                      highlight={lineResult.loading > 80}
                    />
                  </PropertyGroup>
                )}
              </>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <p>No line selected</p>
                <p className="text-xs mt-2">Click on a line to view its properties</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function PropertyGroup({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded border border-gray-200">
      <div className="px-3 py-1.5 bg-gray-50 border-b border-gray-200 text-xs font-medium text-gray-600">
        {title}
      </div>
      <div className="p-2 space-y-1">
        {children}
      </div>
    </div>
  );
}

function PropertyRow({ label, value, highlight = false }: { label: string; value: string; highlight?: boolean }) {
  return (
    <div className="flex justify-between items-center text-sm">
      <span className="text-gray-600">{label}</span>
      <span className={`font-mono ${highlight ? 'text-red-600 font-bold' : 'text-gray-900'}`}>
        {value}
      </span>
    </div>
  );
}

function PropertyInput({ label, value, onChange }: { label: string; value: number; onChange: (v: number) => void }) {
  return (
    <div className="flex justify-between items-center text-sm">
      <span className="text-gray-600">{label}</span>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        className="w-20 px-2 py-0.5 text-right text-sm border border-gray-300 rounded"
        step="0.001"
      />
    </div>
  );
}