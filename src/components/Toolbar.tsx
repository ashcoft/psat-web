'use client';

import { useState } from 'react';

interface ToolbarProps {
  onNew: () => void;
  onOpen: () => void;
  onSave: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFit: () => void;
  onRunPowerFlow: () => void;
  onRunTimeSim: () => void;
  isProcessing: boolean;
}

export default function Toolbar({
  onNew,
  onOpen,
  onSave,
  onUndo,
  onRedo,
  onZoomIn,
  onZoomOut,
  onFit,
  onRunPowerFlow,
  onRunTimeSim,
  isProcessing
}: ToolbarProps) {
  const [history, setHistory] = useState<string[]>(['PSAT v1.0 - Ready']);
  const [status, setStatus] = useState('Ready');

  const ToolbarButton = ({ 
    icon, 
    label, 
    onClick, 
    disabled = false,
    shortcut = ''
  }: { 
    icon: string; 
    label: string; 
    onClick: () => void; 
    disabled?: boolean;
    shortcut?: string;
  }) => (
    <button
      onClick={onClick}
      disabled={disabled}
      className="flex items-center gap-1 px-2 py-1.5 text-sm rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      title={`${label}${shortcut ? ` (${shortcut})` : ''}`}
    >
      <span className="text-base">{icon}</span>
      <span className="hidden md:inline">{label}</span>
    </button>
  );

  return (
    <div className="flex items-center justify-between bg-gray-100 border-b border-gray-300 px-2 py-1">
      {/* Left Section - File Operations */}
      <div className="flex items-center gap-1">
        <ToolbarButton icon="📁" label="New" onClick={onNew} shortcut="Ctrl+N" />
        <ToolbarButton icon="📂" label="Open" onClick={onOpen} shortcut="Ctrl+O" />
        <ToolbarButton icon="💾" label="Save" onClick={onSave} shortcut="Ctrl+S" />
        
        <div className="w-px h-6 bg-gray-300 mx-1" />
        
        <ToolbarButton icon="↩" label="Undo" onClick={onUndo} shortcut="Ctrl+Z" />
        <ToolbarButton icon="↪" label="Redo" onClick={onRedo} shortcut="Ctrl+Y" />
        
        <div className="w-px h-6 bg-gray-300 mx-1" />
        
        <ToolbarButton icon="🔍+" label="Zoom In" onClick={onZoomIn} shortcut="Ctrl++" />
        <ToolbarButton icon="🔍-" label="Zoom Out" onClick={onZoomOut} shortcut="Ctrl+-" />
        <ToolbarButton icon="⬜" label="Fit" onClick={onFit} />
      </div>

      {/* Center Section - Analysis Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={onRunPowerFlow}
          disabled={isProcessing}
          className="flex items-center gap-2 px-4 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
        >
          <span>⚡</span>
          <span>Run Power Flow</span>
          {isProcessing && <span className="animate-spin">⟳</span>}
        </button>
        
        <button
          onClick={onRunTimeSim}
          disabled={isProcessing}
          className="flex items-center gap-2 px-4 py-1.5 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
        >
          <span>⏱</span>
          <span>Time Simulation</span>
        </button>
      </div>

      {/* Right Section - Status */}
      <div className="flex items-center gap-3 text-sm text-gray-600">
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${status === 'Ready' ? 'bg-green-500' : 'bg-yellow-500'}`} />
          <span>{status}</span>
        </div>
        <div className="text-xs text-gray-400">
          {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}