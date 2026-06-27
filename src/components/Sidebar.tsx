'use client';

import { useState, useCallback } from 'react';
import { PowerSystem } from '@/types';
import {
  SlackBusIcon, PVBusIcon, PQBusIcon,
  GeneratorIcon, LoadIcon, ShuntIcon,
  LineIcon, TransformerIcon, FactsIcon,
  AvrIcon, GovernorIcon, PssIcon, LtciIcon,
  AreaIcon, BatteryIcon
} from './SymbolIcons';

interface SidebarProps {
  system: PowerSystem;
  onAddBus: (type: 'slack' | 'pv' | 'pq') => void;
  onAddLine: () => void;
  onAddTransformer: () => void;
  onAddGenerator: () => void;
  onAddLoad: () => void;
  onAddShunt: () => void;
  onCollapse: () => void;
}

interface SectionProps {
  id: string;
  title: string;
  icon: React.ReactNode;
  expandedSection: string | null;
  onToggle: (id: string) => void;
  children: React.ReactNode;
}

function Section({ id, title, icon, expandedSection, onToggle, children }: SectionProps) {
  return (
    <div className="border-b border-gray-200">
      <button
        onClick={() => onToggle(id)}
        className="w-full flex items-center justify-between px-3 py-2 bg-gray-50 hover:bg-gray-100 text-sm font-medium"
      >
        <span className="flex items-center gap-2">
          <span className="flex items-center">{icon}</span>
          <span>{title}</span>
        </span>
        <span className="text-gray-400">{expandedSection === id ? '▼' : '▶'}</span>
      </button>
      {expandedSection === id && (
        <div className="p-2 bg-white">
          {children}
        </div>
      )}
    </div>
  );
}

export default function Sidebar({
  system,
  onAddBus,
  onAddLine,
  onAddTransformer,
  onAddGenerator,
  onAddLoad,
  onAddShunt,
  onCollapse
}: SidebarProps) {
  const [expandedSection, setExpandedSection] = useState<string | null>('buses');
  
  const handleToggle = useCallback((id: string) => {
    setExpandedSection(prev => prev === id ? null : id);
  }, []);

  return (
    <div className="w-64 bg-gray-100 border-r border-gray-300 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-gray-200 border-b border-gray-300">
        <span className="font-medium text-sm">Component Browser</span>
        <button
          onClick={onCollapse}
          className="text-gray-500 hover:text-gray-700 text-lg"
          title="Collapse"
        >
          ×
        </button>
      </div>
      
      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto">
        {/* Buses Section */}
        <Section id="buses" title="Buses" icon={<PQBusIcon size={16} />} expandedSection={expandedSection} onToggle={handleToggle}>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => onAddBus('slack')}
              className="flex flex-col items-center p-2 bg-green-50 rounded hover:bg-green-100"
              title="Add Slack Bus"
            >
              <span className="text-green-600"><SlackBusIcon size={22} /></span>
              <span className="text-xs mt-1">Slack</span>
            </button>
            <button
              onClick={() => onAddBus('pv')}
              className="flex flex-col items-center p-2 bg-blue-50 rounded hover:bg-blue-100"
              title="Add PV Bus"
            >
              <span className="text-blue-600"><PVBusIcon size={22} /></span>
              <span className="text-xs mt-1">PV</span>
            </button>
            <button
              onClick={() => onAddBus('pq')}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add PQ Bus"
            >
              <span className="text-gray-600"><PQBusIcon size={22} /></span>
              <span className="text-xs mt-1">PQ</span>
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {system.buses.length} buses in system
          </div>
        </Section>

        {/* Branches Section */}
        <Section id="branches" title="Branches" icon={<LineIcon size={16} />} expandedSection={expandedSection} onToggle={handleToggle}>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={onAddLine}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Line"
            >
              <span className="text-gray-600"><LineIcon size={22} /></span>
              <span className="text-xs mt-1">Line</span>
            </button>
            <button
              onClick={onAddTransformer}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Transformer"
            >
              <span className="text-gray-600"><TransformerIcon size={22} /></span>
              <span className="text-xs mt-1">Txfr</span>
            </button>
            <button
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add FACTS"
            >
              <span className="text-gray-600"><FactsIcon size={22} /></span>
              <span className="text-xs mt-1">FACTS</span>
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {system.lines.length} lines, {system.transformers.length} transformers
          </div>
        </Section>

        {/* Devices Section */}
        <Section id="devices" title="Devices" icon={<GeneratorIcon size={16} />} expandedSection={expandedSection} onToggle={handleToggle}>
          <div className="grid grid-cols-4 gap-2">
            <button
              onClick={onAddGenerator}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Generator"
            >
              <span className="text-gray-600"><GeneratorIcon size={22} /></span>
              <span className="text-xs">Gen</span>
            </button>
            <button
              onClick={onAddLoad}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Load"
            >
              <span className="text-gray-600"><LoadIcon size={22} /></span>
              <span className="text-xs">Load</span>
            </button>
            <button
              onClick={onAddShunt}
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Shunt"
            >
              <span className="text-gray-600"><ShuntIcon size={22} /></span>
              <span className="text-xs">Shnt</span>
            </button>
            <button
              className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100"
              title="Add Battery"
            >
              <span className="text-gray-600"><BatteryIcon size={22} /></span>
              <span className="text-xs">Batt</span>
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {system.generators.length} generators, {system.loads.length} loads
          </div>
        </Section>

        {/* Controls Section */}
        <Section id="controls" title="Controls" icon={<AvrIcon size={16} />} expandedSection={expandedSection} onToggle={handleToggle}>
          <div className="grid grid-cols-4 gap-2">
            <button className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100" title="AVR">
              <span className="text-gray-600"><AvrIcon size={22} /></span>
              <span className="text-xs">AVR</span>
            </button>
            <button className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100" title="Governor">
              <span className="text-gray-600"><GovernorIcon size={22} /></span>
              <span className="text-xs">Gov</span>
            </button>
            <button className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100" title="PSS">
              <span className="text-gray-600"><PssIcon size={22} /></span>
              <span className="text-xs">PSS</span>
            </button>
            <button className="flex flex-col items-center p-2 bg-gray-50 rounded hover:bg-gray-100" title="LTC">
              <span className="text-gray-600"><LtciIcon size={22} /></span>
              <span className="text-xs">LTC</span>
            </button>
          </div>
        </Section>

        {/* Areas Section */}
        <Section id="areas" title="Areas & Regions" icon={<AreaIcon size={16} />} expandedSection={expandedSection} onToggle={handleToggle}>
          <div className="space-y-2">
            {(system.areas || []).map(area => (
              <div key={area.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <span className="text-sm">{area.name}</span>
                <span className="text-xs text-gray-500">#{area.id}</span>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
