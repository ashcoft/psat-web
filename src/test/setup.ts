import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver
class ResizeObserverMock {
  // eslint-disable-next-line @typescript-eslint/no-empty-object-pattern
  observe() {
    // Mock observe implementation
  }
  // eslint-disable-next-line @typescript-eslint/no-empty-object-pattern
  unobserve() {
    // Mock unobserve implementation
  }
  // eslint-disable-next-line @typescript-eslint/no-empty-object-pattern
  disconnect() {
    // Mock disconnect implementation
  }
}
window.ResizeObserver = ResizeObserverMock;

// Mock HTMLCanvasElement
// eslint-disable-next-line @typescript-eslint/no-explicit-any
(HTMLCanvasElement.prototype as any).getContext = () => {
  const noop = () => {
    // noop
  };
  return {
    fillRect: noop,
    clearRect: noop,
    getImageData: () => ({ data: [], width: 0, height: 0 }),
    putImageData: noop,
    createImageData: () => ({ data: [], width: 0, height: 0 }),
    setTransform: noop,
    drawImage: noop,
    save: noop,
    restore: noop,
    beginPath: noop,
    moveTo: noop,
    lineTo: noop,
    closePath: noop,
    stroke: noop,
    fill: noop,
    translate: noop,
    scale: noop,
    rotate: noop,
    arc: noop,
    measureText: () => ({ width: 0 }),
  };
};
