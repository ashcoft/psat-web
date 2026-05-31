'use client';

import { useState } from 'react';

interface Tab {
  id: string;
  label: string;
  groups: ButtonGroup[];
}

interface ButtonGroup {
  label: string;
  buttons: Button[];
}

interface Button {
  id: string;
  icon: string;
  label: string;
  action: string;
  shortcut?: string;
}

interface RibbonProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
  onAction: (action: string) => void;
}

const tabs: Tab[] = [
  {
    id: 'home',
    label: 'Home',
    groups: [
      {
        label: 'File',
        buttons: [
          { id: 'open', icon: '📂', label: 'Open', action: 'open' },
          { id: 'save', icon: '💾', label: 'Save', action: 'save', shortcut: 'Ctrl+S' },
          { id: 'export', icon: '📤', label: 'Export', action: 'export' },
        ]
      },
      {
        label: 'Edit',
        buttons: [
          { id: 'undo', icon: '↩', label: 'Undo', action: 'undo', shortcut: 'Ctrl+Z' },
          { id: 'redo', icon: '↪', label: 'Redo', action: 'redo', shortcut: 'Ctrl+Y' },
          { id: 'copy', icon: '📋', label: 'Copy', action: 'copy', shortcut: 'Ctrl+C' },
          { id: 'paste', icon: '📨', label: 'Paste', action: 'paste', shortcut: 'Ctrl+V' },
        ]
      },
      {
        label: 'View',
        buttons: [
          { id: 'zoom-in', icon: '🔍+', label: 'Zoom In', action: 'zoom-in' },
          { id: 'zoom-out', icon: '🔍-', label: 'Zoom Out', action: 'zoom-out' },
          { id: 'fit', icon: '⬜', label: 'Fit', action: 'fit' },
        ]
      }
    ]
  },
  {
    id: 'analysis',
    label: 'Analysis',
    groups: [
      {
        label: 'Power Flow',
        buttons: [
          { id: 'lf', icon: '⚡', label: 'Power Flow', action: 'power-flow', shortcut: 'F5' },
          { id: 'cpf', icon: '📈', label: 'Continuation PF', action: 'cpf' },
          { id: 'opf', icon: '📊', label: 'Optimal PF', action: 'opf' },
        ]
      },
      {
        label: 'Dynamics',
        buttons: [
          { id: 'time', icon: '⏱', label: 'Time Simulation', action: 'time-sim' },
          { id: 'eigen', icon: '📉', label: 'Eigenvalue', action: 'eigenvalue' },
          { id: 'modal', icon: '📐', label: 'Modal Analysis', action: 'modal' },
        ]
      }
    ]
  },
  {
    id: 'components',
    label: 'Components',
    groups: [
      {
        label: 'Buses',
        buttons: [
          { id: 'bus-slack', icon: '◯', label: 'Slack Bus', action: 'add-slack' },
          { id: 'bus-pv', icon: '◐', label: 'PV Bus', action: 'add-pv' },
          { id: 'bus-pq', icon: '○', label: 'PQ Bus', action: 'add-pq' },
        ]
      },
      {
        label: 'Branches',
        buttons: [
          { id: 'line', icon: '/', label: 'Line', action: 'add-line' },
          { id: 'transformer', icon: '⊣', label: 'Transformer', action: 'add-transformer' },
        ]
      },
      {
        label: 'Devices',
        buttons: [
          { id: 'gen', icon: '⊛', label: 'Generator', action: 'add-generator' },
          { id: 'load', icon: '▤', label: 'Load', action: 'add-load' },
          { id: 'shunt', icon: '⊞', label: 'Shunt', action: 'add-shunt' },
        ]
      }
    ]
  },
  {
    id: 'tools',
    label: 'Tools',
    groups: [
      {
        label: 'Reports',
        buttons: [
          { id: 'report', icon: '📄', label: 'Report', action: 'report' },
          { id: 'summary', icon: '📋', label: 'Summary', action: 'summary' },
        ]
      },
      {
        label: 'Settings',
        buttons: [
          { id: 'settings', icon: '⚙', label: 'Settings', action: 'settings' },
          { id: 'themes', icon: '🎨', label: 'Themes', action: 'themes' },
        ]
      }
    ]
  }
];

export default function Ribbon({ activeTab, onTabChange, onAction }: RibbonProps) {
  const [expandedGroup, setExpandedGroup] = useState<string | null>(null);
  
  const currentTab = tabs.find(t => t.id === activeTab) || tabs[0];
  
  return (
    <div className="flex flex-col bg-gray-100 border-b border-gray-300">
      {/* Tab Bar */}
      <div className="flex bg-gray-200 border-b border-gray-300">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-white border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      
      {/* Ribbon Content */}
      <div className="bg-gray-50 p-2 min-h-[80px]">
        {currentTab.groups.map((group, gIdx) => (
          <div key={gIdx} className="inline-block align-top mr-4 mb-2">
            <div className="text-xs text-gray-500 font-medium px-1 mb-1">{group.label}</div>
            <div className="flex gap-1">
              {group.buttons.map(btn => (
                <button
                  key={btn.id}
                  onClick={() => onAction(btn.action)}
                  className="flex flex-col items-center px-2 py-1 rounded hover:bg-blue-100 transition-colors group relative"
                  title={`${btn.label}${btn.shortcut ? ` (${btn.shortcut})` : ''}`}
                >
                  <span className="text-xl">{btn.icon}</span>
                  <span className="text-xs text-gray-600">{btn.label}</span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}