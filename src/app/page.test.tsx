import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import HomePage from './page';

// Mock the Canvas component
vi.mock('@/components/Canvas', () => ({
  default: () => <div data-testid="canvas">Canvas</div>,
}));

// Mock the Ribbon component
vi.mock('@/components/Ribbon', () => ({
  default: () => <div data-testid="ribbon">Ribbon</div>,
}));

// Mock the Toolbar component
vi.mock('@/components/Toolbar', () => ({
  default: () => <div data-testid="toolbar">Toolbar</div>,
}));

// Mock the Sidebar component
vi.mock('@/components/Sidebar', () => ({
  default: () => <div data-testid="sidebar">Sidebar</div>,
}));

// Mock the PropertiesPanel component
vi.mock('@/components/PropertiesPanel', () => ({
  default: () => <div data-testid="properties-panel">Properties Panel</div>,
}));

// Mock the OutputWindow component
vi.mock('@/components/OutputWindow', () => ({
  default: () => <div data-testid="output-window">Output Window</div>,
}));

// Mock the SettingsDialog component
vi.mock('@/components/SettingsDialog', () => ({
  default: () => <div data-testid="settings-dialog">Settings Dialog</div>,
}));

describe('HomePage', () => {
  it('should render without crashing', () => {
    render(<HomePage />);
    expect(screen.getByText('⚡ PSAT')).toBeInTheDocument();
  });

  it('should display the title', () => {
    render(<HomePage />);
    expect(screen.getByText('Power System Analysis Toolbox')).toBeInTheDocument();
  });

  it('should render all main components', () => {
    render(<HomePage />);
    expect(screen.getByTestId('ribbon')).toBeInTheDocument();
    expect(screen.getByTestId('toolbar')).toBeInTheDocument();
    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    expect(screen.getByTestId('canvas')).toBeInTheDocument();
    expect(screen.getByTestId('output-window')).toBeInTheDocument();
    expect(screen.getByTestId('properties-panel')).toBeInTheDocument();
  });

  it('should display initial status bar information', () => {
    render(<HomePage />);
    expect(screen.getByText(/Buses:/)).toBeInTheDocument();
    expect(screen.getByText(/Lines:/)).toBeInTheDocument();
    expect(screen.getByText(/Transformers:/)).toBeInTheDocument();
    expect(screen.getByText(/Loads:/)).toBeInTheDocument();
    expect(screen.getByText(/Generators:/)).toBeInTheDocument();
    expect(screen.getByText(/Base: 100 MVA/)).toBeInTheDocument();
    expect(screen.getByText(/Frequency: 50 Hz/)).toBeInTheDocument();
  });

  it('should have menu items in title bar', () => {
    render(<HomePage />);
    expect(screen.getByText('File')).toBeInTheDocument();
    expect(screen.getByText('Edit')).toBeInTheDocument();
    expect(screen.getByText('View')).toBeInTheDocument();
    expect(screen.getByText('Analysis')).toBeInTheDocument();
    expect(screen.getByText('Help')).toBeInTheDocument();
  });
});
