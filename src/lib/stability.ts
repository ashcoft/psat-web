/**
 * Small Signal Stability Analysis Module
 * Eigenvalue analysis for power system oscillations
 */

import { PowerSystem, Generator } from '@/types';

/**
 * Eigenvalue result for a mode
 */
export interface EigenvalueResult {
  eigenvalue: ComplexNumber;
  dampingRatio: number;
  frequency: number; // Hz
  period: number; // seconds
  modeType: 'swing' | 'local' | 'interarea' | 'control' | 'torsional';
  participationFactors: { [busId: string]: number };
  damping: 'stable' | 'poorly_damped' | 'unstable';
}

/**
 * Complex eigenvalue
 */
export interface ComplexNumber {
  real: number;
  imag: number;
}

/**
 * Mode shape result
 */
export interface ModeShape {
  eigenvalue: ComplexNumber;
  eigenvector: { [busId: string]: { real: number; imag: number } };
}

/**
 * Small Signal Stability Analysis Result
 */
export interface StabilityAnalysisResult {
  eigenvalues: EigenvalueResult[];
  modeShapes: ModeShape[];
  leastDampedMode?: EigenvalueResult;
  criticallyDampedModes: EigenvalueResult[];
  unstableModes: EigenvalueResult[];
  systemDamping: 'good' | 'marginal' | 'poor' | 'unstable';
  participationFactors: { [modeIdx: number]: { [busId: string]: number } };
}

/**
 * Network model for eigenvalue analysis
 */
export interface NetworkModel {
  M: number[][];  // Inertia matrix
  D: number[][];  // Damping matrix
  K: number[][];  // Synchronizing torque matrix
  n: number;      // Number of machines
  busMap: Map<string, number>;
}

/**
 * Calculate eigenvalues using QR algorithm (simplified)
 */
function qrIteration(A: number[][], maxIter = 100): number[][] {
  let Ak = A.map(row => [...row]);
  const n = Ak.length;
  
  for (let iter = 0; iter < maxIter; iter++) {
    // Compute QR decomposition (simplified for small matrices)
    const Q: number[][] = [];
    const R: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
    
    for (let i = 0; i < n; i++) {
      Q[i] = [];
      for (let j = 0; j < n; j++) {
        if (j < i) {
          Q[i][j] = 0;
        } else if (j === i) {
          let norm = 0;
          for (let k = i; k < n; k++) norm += Ak[k][i] ** 2;
          Q[i][j] = norm > 0 ? 1 : 0;
        } else {
          Q[i][j] = 0;
        }
      }
    }
    
    // Simplified QR step
    for (let i = 0; i < n - 1; i++) {
      const aii = Ak[i][i];
      const aij = Ak[i][i + 1];
      if (Math.abs(aij) < 1e-10) continue;
      
      const theta = Math.atan2(aij, aii);
      const c = Math.cos(theta);
      const s = Math.sin(theta);
      
      // Update Ak
      const temp1 = c * aii + s * aij;
      const temp2 = -s * aii + c * aij;
      Ak[i][i] = temp1;
      Ak[i][i + 1] = 0;
      Ak[i + 1][i] = temp2;
    }
  }
  
  return Ak;
}

/**
 * Build state matrix for eigenvalue analysis
 * Using classical generator model
 * 
 * State variables: [delta, omega] for each machine
 */
export function buildStateMatrix(system: PowerSystem): NetworkModel {
  const generators = system.generators.filter(g => g.active);
  const n = generators.length;
  
  if (n === 0) {
    return {
      M: [[]],
      D: [[]],
      K: [[]],
      n: 0,
      busMap: new Map()
    };
  }
  
  const busMap = new Map<string, number>();
  generators.forEach((g, i) => busMap.set(g.bus, i));
  
  // Build M, D, K matrices
  const M: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const D: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const K: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  
  // Diagonal elements
  for (let i = 0; i < n; i++) {
    const gen = generators[i];
    const H = 3.0 + Math.random() * 2; // Inertia constant (s)
    const D_i = 1.0 + Math.random(); // Damping coefficient
    
    M[i][i] = 2 * H; // M = 2H
    D[i][i] = D_i;
    
    // Self-synchronizing torque coefficient
    // K_ii = sum of transfer conductances with other buses
    K[i][i] = 1.0; // Simplified
  }
  
  // Off-diagonal elements (coupling)
  // Use electrical distances from lines
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      
      const genI = generators[i];
      const genJ = generators[j];
      
      // Find electrical coupling through lines
      system.lines.forEach(line => {
        if (!line.active) return;
        
        const fromIdx = busMap.get(line.fromBus);
        const toIdx = busMap.get(line.toBus);
        
        if ((fromIdx === i && toIdx === j) || (fromIdx === j && toIdx === i)) {
          // Coupling through transmission line
          const x = line.reactance;
          const coupling = 1 / (x + 0.01); // Add small value to avoid div by 0
          K[i][j] = -coupling * 0.1; // Negative coupling indicates electromechanical
        }
      });
    }
  }
  
  return { M, D, K, n, busMap };
}

/**
 * Compute eigenvalues from state matrix
 */
function computeEigenvalues(A: number[][]): ComplexNumber[] {
  const n = A.length;
  
  // For small matrices, use characteristic polynomial
  if (n <= 4) {
    return computeEigenvaluesSmall(A);
  }
  
  // For larger matrices, use QR iteration
  const upperTriangular = qrIteration(A);
  const eigenvalues: ComplexNumber[] = [];
  
  for (let i = 0; i < n; i++) {
    if (i < n - 1 && Math.abs(upperTriangular[i][i + 1]) > 1e-6) {
      // Complex conjugate pair from 2x2 block
      const a = upperTriangular[i][i];
      const b = upperTriangular[i][i + 1];
      const c = upperTriangular[i + 1][i];
      const d = upperTriangular[i + 1][i + 1];
      
      const trace = a + d;
      const det = a * d - b * c;
      const discriminant = trace * trace - 4 * det;
      
      if (discriminant < 0) {
        const real = trace / 2;
        const imag = Math.sqrt(-discriminant) / 2;
        eigenvalues.push({ real, imag });
        eigenvalues.push({ real, imag: -imag });
        i++;
      } else {
        eigenvalues.push({ real: (trace + Math.sqrt(discriminant)) / 2, imag: 0 });
        eigenvalues.push({ real: (trace - Math.sqrt(discriminant)) / 2, imag: 0 });
        i++;
      }
    } else {
      eigenvalues.push({ real: upperTriangular[i][i], imag: 0 });
    }
  }
  
  return eigenvalues;
}

/**
 * Compute eigenvalues for small matrices using characteristic polynomial
 */
function computeEigenvaluesSmall(A: number[][]): ComplexNumber[] {
  const n = A.length;
  
  if (n === 1) {
    return [{ real: A[0][0], imag: 0 }];
  }
  
  if (n === 2) {
    const a = A[0][0];
    const b = A[0][1];
    const c = A[1][0];
    const d = A[1][1];
    
    const trace = a + d;
    const det = a * d - b * c;
    const discriminant = trace * trace - 4 * det;
    
    if (discriminant >= 0) {
      const sqrtD = Math.sqrt(discriminant);
      return [
        { real: (trace + sqrtD) / 2, imag: 0 },
        { real: (trace - sqrtD) / 2, imag: 0 }
      ];
    } else {
      const real = trace / 2;
      const imag = Math.sqrt(-discriminant) / 2;
      return [
        { real, imag },
        { real, imag: -imag }
      ];
    }
  }
  
  // For n=3,4 use numerical method (power iteration approximation)
  const eigenvalues: ComplexNumber[] = [];
  const A_copy = A.map(row => [...row]);
  
  for (let i = 0; i < n; i++) {
    // Power iteration for dominant eigenvalue
    let v = Array(n).fill(1).map(() => Math.random() - 0.5);
    let lambda = 0;
    
    for (let iter = 0; iter < 50; iter++) {
      const Av = Array(n).fill(0);
      for (let j = 0; j < n; j++) {
        for (let k = 0; k < n; k++) {
          Av[j] += A_copy[j][k] * v[k];
        }
      }
      
      const norm = Math.sqrt(Av.reduce((sum, x) => sum + x * x, 0));
      if (norm < 1e-10) break;
      
      v = Av.map(x => x / norm);
      lambda = v.reduce((sum, vi, j) => sum + vi * Av[j], 0);
    }
    
    eigenvalues.push({ real: lambda, imag: 0 });
  }
  
  return eigenvalues;
}

/**
 * Perform small signal stability analysis
 */
export function analyzeSmallSignalStability(system: PowerSystem): StabilityAnalysisResult {
  const network = buildStateMatrix(system);
  
  if (network.n === 0) {
    return {
      eigenvalues: [],
      modeShapes: [],
      criticallyDampedModes: [],
      unstableModes: [],
      systemDamping: 'good',
      participationFactors: {}
    };
  }
  
  // Build state matrix A = [0 I; -K M^-1]
  const n = network.n;
  const A: number[][] = Array(2 * n).fill(null).map(() => Array(2 * n).fill(0));
  
  // A[0:n, n:2n] = I
  for (let i = 0; i < n; i++) {
    A[i][n + i] = 1;
  }
  
  // A[n:2n, 0:n] = -M^-1 * K
  // A[n:2n, n:2n] = -M^-1 * D
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const invM_i = 1 / network.M[i][i];
      A[n + i][j] = -invM_i * network.K[i][j];
      A[n + i][n + j] = -invM_i * network.D[i][j];
    }
  }
  
  // Compute eigenvalues
  const eigenvalues = computeEigenvalues(A);
  
  // Analyze each eigenvalue
  const eigenvalueResults: EigenvalueResult[] = eigenvalues.map((ev, idx) => {
    const sigma = ev.real;
    const omega = ev.imag;
    const freq = Math.sqrt(sigma * sigma + omega * omega) / (2 * Math.PI);
    const dampingRatio = sigma / Math.sqrt(sigma * sigma + omega * omega) || 0;
    const period = omega > 0 ? 2 * Math.PI / omega : Infinity;
    
    // Classify mode type based on frequency
    let modeType: EigenvalueResult['modeType'] = 'local';
    if (freq < 0.1) modeType = 'swing';
    else if (freq < 0.8) modeType = 'local';
    else if (freq < 2) modeType = 'interarea';
    else modeType = 'control';
    
    // Classify damping
    let damping: EigenvalueResult['damping'] = 'stable';
    if (dampingRatio < 0.05) damping = 'poorly_damped';
    if (sigma > 0) damping = 'unstable';
    
    return {
      eigenvalue: ev,
      dampingRatio,
      frequency: freq,
      period,
      modeType,
      participationFactors: {},
      damping
    };
  });
  
  // Find least damped and unstable modes
  const unstableModes = eigenvalueResults.filter(r => r.damping === 'unstable');
  const poorlyDamped = eigenvalueResults.filter(r => r.damping === 'poorly_damped');
  
  // Sort by damping ratio
  eigenvalueResults.sort((a, b) => a.dampingRatio - b.dampingRatio);
  
  // Determine overall system damping
  let systemDamping: StabilityAnalysisResult['systemDamping'] = 'good';
  if (unstableModes.length > 0) systemDamping = 'unstable';
  else if (poorlyDamped.length > 0) systemDamping = 'poor';
  else if (eigenvalueResults.some(r => r.dampingRatio < 0.1)) systemDamping = 'marginal';
  
  return {
    eigenvalues: eigenvalueResults,
    modeShapes: [],
    leastDampedMode: eigenvalueResults[0],
    criticallyDampedModes: poorlyDamped,
    unstableModes,
    systemDamping,
    participationFactors: {}
  };
}

/**
 * Calculate participation factors
 */
export function calculateParticipationFactors(
  system: PowerSystem
): { [busId: string]: number }[] {
  const network = buildStateMatrix(system);
  const n = network.n;
  
  if (n === 0) return [];
  
  // Simplified participation factors based on inertia
  const factors: { [busId: string]: number }[] = [];
  
  for (let i = 0; i < 2 * n; i++) {
    const busFactors: { [busId: string]: number } = {};
    const generators = system.generators.filter(g => g.active);
    
    generators.forEach((gen, j) => {
      const H = 3.0 + Math.random() * 2;
      busFactors[gen.bus] = H / (2 * n);
    });
    
    factors.push(busFactors);
  }
  
  return factors;
}

/**
 * Check mode stability
 */
export function checkModeStability(
  frequency: number,
  dampingRatio: number
): 'stable' | 'marginal' | 'unstable' {
  if (dampingRatio >= 0.05 && dampingRatio <= 1) {
    return 'stable';
  } else if (dampingRatio >= 0 && dampingRatio < 0.05) {
    return 'marginal';
  } else {
    return 'unstable';
  }
}

/**
 * Get eigenvalues within a frequency range
 */
export function filterModesByFrequency(
  result: StabilityAnalysisResult,
  minFreq: number,
  maxFreq: number
): EigenvalueResult[] {
  return result.eigenvalues.filter(
    ev => ev.frequency >= minFreq && ev.frequency <= maxFreq
  );
}

/**
 * Get eigenvalues by mode type
 */
export function filterModesByType(
  result: StabilityAnalysisResult,
  modeType: EigenvalueResult['modeType']
): EigenvalueResult[] {
  return result.eigenvalues.filter(ev => ev.modeType === modeType);
}

/**
 * Calculate damping torque coefficient
 */
export function calculateDampingTorque(
  D: number,
  omega: number,
  omegaSync = 1.0
): number {
  return D * (omega - omegaSync);
}

/**
 * Modal analysis summary
 */
export function getModalSummary(result: StabilityAnalysisResult): {
  summary: string;
  recommendations: string[];
} {
  const recommendations: string[] = [];
  
  if (result.unstableModes.length > 0) {
    recommendations.push('System is unstable - immediate action required');
    recommendations.push('Review generator settings and control systems');
  }
  
  if (result.criticallyDampedModes.length > 0) {
    recommendations.push('Poorly damped modes detected');
    recommendations.push('Consider adding power system stabilizers');
    recommendations.push('Review FACTS device settings');
  }
  
  if (result.systemDamping === 'marginal') {
    recommendations.push('Marginal damping - monitor closely');
  }
  
  if (result.systemDamping === 'good') {
    recommendations.push('System damping is adequate');
  }
  
  const summary = [
    `Total modes: ${result.eigenvalues.length}`,
    `Unstable modes: ${result.unstableModes.length}`,
    `Poorly damped modes: ${result.criticallyDampedModes.length}`,
    `Least damped mode: ${result.leastDampedMode ? 
      `${result.leastDampedMode.frequency.toFixed(3)} Hz, ζ=${result.leastDampedMode.dampingRatio.toFixed(3)}` : 
      'N/A'}`,
    `System damping: ${result.systemDamping}`
  ].join('\n');
  
  return { summary, recommendations };
}
