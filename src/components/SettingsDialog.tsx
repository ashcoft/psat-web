'use client';

import { useState } from 'react';

interface SettingsDialogProps {
  onClose: () => void;
}

export default function SettingsDialog({ onClose }: SettingsDialogProps) {
  const [settings, setSettings] = useState({
    baseFrequency: 50,
    basePower: 100,
    tolerance: 1e-6,
    maxIterations: 100,
    solutionMethod: 'nr',
    flatStart: true,
    beeps: false,
    theme: 'light',
    voltageMin: 0.9,
    voltageMax: 1.1,
  });

  const handleSave = () => {
    // In a real app, this would save settings to localStorage or server
    console.log('Saving settings:', settings);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-[500px] max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-blue-600 text-white">
          <h2 className="text-lg font-medium">Settings</h2>
          <button
            onClick={onClose}
            className="text-2xl hover:opacity-80"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-y-auto max-h-[60vh]">
          <div className="space-y-6">
            {/* General Section */}
            <SettingsSection title="General">
              <SettingsRow label="Base Frequency (Hz)">
                <input
                  type="number"
                  value={settings.baseFrequency}
                  onChange={(e) => setSettings({ ...settings, baseFrequency: parseFloat(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                />
              </SettingsRow>
              <SettingsRow label="Base Power (MVA)">
                <input
                  type="number"
                  value={settings.basePower}
                  onChange={(e) => setSettings({ ...settings, basePower: parseFloat(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                />
              </SettingsRow>
              <SettingsRow label="Theme">
                <select
                  value={settings.theme}
                  onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="custom">Custom</option>
                </select>
              </SettingsRow>
            </SettingsSection>

            {/* Power Flow Section */}
            <SettingsSection title="Power Flow">
              <SettingsRow label="Solution Method">
                <select
                  value={settings.solutionMethod}
                  onChange={(e) => setSettings({ ...settings, solutionMethod: e.target.value })}
                  className="w-32 px-2 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value="nr">Newton-Raphson</option>
                  <option value="dc">DC Power Flow</option>
                  <option value="fast-decoupled">Fast Decoupled</option>
                </select>
              </SettingsRow>
              <SettingsRow label="Tolerance">
                <input
                  type="number"
                  value={settings.tolerance}
                  onChange={(e) => setSettings({ ...settings, tolerance: parseFloat(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                  step="0.0001"
                />
              </SettingsRow>
              <SettingsRow label="Max Iterations">
                <input
                  type="number"
                  value={settings.maxIterations}
                  onChange={(e) => setSettings({ ...settings, maxIterations: parseInt(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                />
              </SettingsRow>
              <SettingsRow label="Flat Start">
                <input
                  type="checkbox"
                  checked={settings.flatStart}
                  onChange={(e) => setSettings({ ...settings, flatStart: e.target.checked })}
                  className="w-4 h-4"
                />
              </SettingsRow>
            </SettingsSection>

            {/* Voltage Limits Section */}
            <SettingsSection title="Voltage Limits">
              <SettingsRow label="Vmin (pu)">
                <input
                  type="number"
                  value={settings.voltageMin}
                  onChange={(e) => setSettings({ ...settings, voltageMin: parseFloat(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                  step="0.01"
                />
              </SettingsRow>
              <SettingsRow label="Vmax (pu)">
                <input
                  type="number"
                  value={settings.voltageMax}
                  onChange={(e) => setSettings({ ...settings, voltageMax: parseFloat(e.target.value) })}
                  className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                  step="0.01"
                />
              </SettingsRow>
            </SettingsSection>

            {/* Miscellaneous Section */}
            <SettingsSection title="Miscellaneous">
              <SettingsRow label="Beeps">
                <input
                  type="checkbox"
                  checked={settings.beeps}
                  onChange={(e) => setSettings({ ...settings, beeps: e.target.checked })}
                  className="w-4 h-4"
                />
              </SettingsRow>
            </SettingsSection>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-2 px-4 py-3 bg-gray-50 border-t">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

function SettingsSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="text-sm font-medium text-gray-700 mb-2 border-b pb-1">{title}</h3>
      <div className="space-y-2">
        {children}
      </div>
    </div>
  );
}

function SettingsRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-gray-600">{label}</span>
      {children}
    </div>
  );
}