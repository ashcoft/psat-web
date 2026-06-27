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
 * Per §3 contract:
 *   Y_ij (off-diagonal, i≠j) = −y_series_ij  ← NEGATIVE of series admittance
 *   Y_ii (diagonal)          = Σ y_series_ik  +  jB_c/2  +  y_shunt_i
 */
export function buildYBus(system: PowerSystem): YBusMatrix {
  const n = system.buses.length;
  const g: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  const b: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Add line contributions (π-model)
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i === undefined || j === undefined) return;

    const r = line.resistance;
    const x = line.reactance;
    const z2 = r * r + x * x;
    const yij_real = r / z2;       // gij = R/(R²+X²)
    const yij_imag = -x / z2;     // bij = -X/(R²+X²) (negative for inductive)
    const b_shunt = line.susceptance * 0.5;  // half-line charging B_c/2

    // Off-diagonal: Y_ij = −yij (NEGATIVE series admittance)
    g[i][j] -= yij_real;
    b[i][j] -= yij_imag;
    g[j][i] -= yij_real;
    b[j][i] -= yij_imag;

    // Diagonal: Y_ii += yij + j·B_c/2
    g[i][i] += yij_real;
    b[i][i] += yij_imag + b_shunt;
    g[j][j] += yij_real;
    b[j][j] += yij_imag + b_shunt;
  });

  // Add transformer contributions
  // For transformer with off-nominal tap a = V_from / V_to:
  //   Y_ii (tap side)   += yt / a²
  //   Y_jj (load side)  += yt
  //   Y_ij = Y_ji       -= yt / a
  (system.transformers || []).forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus);
    const j = busIndex.get(txf.toBus);
    if (i === undefined || j === undefined) return;

    const r = txf.resistance;
    const x = txf.reactance;
    const z2 = r * r + x * x;
    const yt_real = r / z2;
    const yt_imag = -x / z2;
    const a = txf.tap > 0 ? txf.tap : 1.0;
    const a2 = a * a;

    // Off-diagonal: Y_ij = Y_ji = −yt/a
    g[i][j] -= yt_real / a;
    b[i][j] -= yt_imag / a;
    g[j][i] -= yt_real / a;
    b[j][i] -= yt_imag / a;

    // Diagonal
    g[i][i] += yt_real / a2;
    b[i][i] += yt_imag / a2;
    g[j][j] += yt_real;
    b[j][j] += yt_imag;
  });

  // Add shunt contributions (go ONLY on the diagonal)
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
 * Per §4C: Build B' DIRECTLY from branch reactances, not from YBus.b
 */
export function solveDC(system: PowerSystem): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  
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

  // Build P injection vector (net power at each bus in MW)
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

  // Build B' matrix DIRECTLY from branch reactances (NOT from YBus.b)
  // Per §4C contract: b_ij_prime = -1 / X_ij
  const B: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  
  // Add lines
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i === undefined || j === undefined) return;
    
    const x = line.reactance;
    if (Math.abs(x) < 1e-10) return; // Skip zero reactance
    
    const b_ij = -1 / x;  // b_ij_prime = -1/X
    
    B[i][i] += b_ij;
    B[j][j] += b_ij;
    B[i][j] -= b_ij;
    B[j][i] -= b_ij;
  });
  
  // Add transformers
  (system.transformers || []).forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus);
    const j = busIndex.get(txf.toBus);
    if (i === undefined || j === undefined) return;
    
    const x = txf.reactance;
    if (Math.abs(x) < 1e-10) return;
    
    const b_ij = -1 / x;
    
    B[i][i] += b_ij;
    B[j][j] += b_ij;
    B[i][j] -= b_ij;
    B[j][i] -= b_ij;
  });

  // Remove slack bus row and column
  const m = n - 1;
  const Bred: number[][] = new Array(m).fill(null).map(() => new Array(m).fill(0));
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

  // Solve linear system Bred * theta = P (in radians)
  const theta = solveLinearSystem(Bred, Pred);

  // Reconstruct full angle vector
  const angles = new Array(n).fill(0);
  angles[slackIdx] = (system.buses[slackIdx].angle || 0) * Math.PI / 180;
  for (let i = 0; i < m; i++) {
    angles[idxMap[i]] = theta[i];
  }

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const dij = angles[i] - angles[j];
    const x = line.reactance;
    const Pij = dij / x * (system.baseMVA || 100);
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
 * Per §4B: B' is built DIRECTLY from branch reactances
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

  // Build B' matrix DIRECTLY from branch reactances (per §4B contract)
  // b_ij_prime = -1 / X_ij
  const Bp: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i === undefined || j === undefined) return;
    const x = line.reactance;
    if (Math.abs(x) < 1e-10) return;
    const b_ij = -1 / x;
    Bp[i][i] += b_ij;
    Bp[j][j] += b_ij;
    Bp[i][j] -= b_ij;
    Bp[j][i] -= b_ij;
  });
  
  (system.transformers || []).forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus);
    const j = busIndex.get(txf.toBus);
    if (i === undefined || j === undefined) return;
    const x = txf.reactance;
    if (Math.abs(x) < 1e-10) return;
    const b_ij = -1 / x;
    Bp[i][i] += b_ij;
    Bp[j][j] += b_ij;
    Bp[i][j] -= b_ij;
    Bp[j][i] -= b_ij;
  });

  // Build B'' matrix from YBus (for Q-V coupling)
  // B''[i][j] = -YBus.b[i][j] for i≠j
  // B''[i][i] = -YBus.b[i][i] + line_charging
  const Bpp: number[][] = new Array(n).fill(null).map(() => new Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      Bpp[i][j] = -ybus.b[i][j];
    }
  }
  // Add line charging to diagonal
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i !== undefined) Bpp[i][i] += line.susceptance * 0.5;
    if (j !== undefined) Bpp[j][j] += line.susceptance * 0.5;
  });

  // Non-slack bus indices
  const nonSlackBuses: number[] = [];
  for (let i = 0; i < n; i++) {
    if (i !== slackIdx) nonSlackBuses.push(i);
  }
  const m = nonSlackBuses.length;
  
  // Reduced B' matrix
  const Bpred: number[][] = new Array(m).fill(null).map(() => new Array(m).fill(0));
  for (let p = 0; p < m; p++) {
    for (let q = 0; q < m; q++) {
      Bpred[p][q] = Bp[nonSlackBuses[p]][nonSlackBuses[q]];
    }
  }

  // PQ bus indices for B''
  const pqBuses: number[] = [];
  for (let i = 0; i < n; i++) {
    if (i !== slackIdx && system.buses[i].type === 'pq') {
      pqBuses.push(i);
    }
  }
  const nPQ = pqBuses.length;
  
  // Reduced B'' matrix
  const Bppred: number[][] = new Array(nPQ).fill(null).map(() => new Array(nPQ).fill(0));
  for (let p = 0; p < nPQ; p++) {
    for (let q = 0; q < nPQ; q++) {
      Bppred[p][q] = Bpp[pqBuses[p]][pqBuses[q]];
    }
  }

  // Target P and Q
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

  // Iterations
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

    // P mismatch for non-slack buses
    const dP: number[] = [];
    for (const i of nonSlackBuses) {
      dP.push((P[i] - Pcalc[i]) / V[i]);
    }

    // Update angles (P-θ)
    const dTheta = solveLinearSystem(Bpred, dP);
    for (let k = 0; k < nonSlackBuses.length; k++) {
      theta[nonSlackBuses[k]] += dTheta[k];
    }

    // Recalculate after angle update
    for (let i = 0; i < n; i++) {
      Pcalc[i] = 0;
      Qcalc[i] = 0;
      for (let j = 0; j < n; j++) {
        const Vij = V[i] * V[j];
        const theta_ij = theta[i] - theta[j];
        Pcalc[i] += Vij * (ybus.g[i][j] * Math.cos(theta_ij) + ybus.b[i][j] * Math.sin(theta_ij));
        Qcalc[i] += Vij * (ybus.g[i][j] * Math.sin(theta_ij) - ybus.b[i][j] * Math.cos(theta_ij));
      }
    }

    // Q mismatch for PQ buses
    const dQ: number[] = [];
    for (const i of pqBuses) {
      dQ.push((Q[i] - Qcalc[i]) / V[i]);
    }

    // Update voltages (Q-V)
    const dV = solveLinearSystem(Bppred, dQ);
    for (let k = 0; k < pqBuses.length; k++) {
      V[pqBuses[k]] += dV[k];
      V[pqBuses[k]] = Math.max(0.5, Math.min(1.5, V[pqBuses[k]]));
    }

    // Check convergence
    maxMismatch = 0;
    for (const i of nonSlackBuses) {
      maxMismatch = Math.max(maxMismatch, Math.abs(P[i] - Pcalc[i]));
    }
    for (const i of pqBuses) {
      maxMismatch = Math.max(maxMismatch, Math.abs(Q[i] - Qcalc[i]));
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
    
    const dij = theta[i] - theta[j];
    const z2 = line.resistance * line.resistance + line.reactance * line.reactance;
    const y_real = line.resistance / z2;
    const y_imag = -line.reactance / z2;
    
    const Vi = V[i];
    const Vj = V[j];
    const Pij = Vi * Vj * (y_real * Math.cos(dij) + y_imag * Math.sin(dij));
    const Qij = Vi * Vj * (y_real * Math.sin(dij) - y_imag * Math.cos(dij));
    const Pji = Vi * Vj * (y_real * Math.cos(-dij) + y_imag * Math.sin(-dij));
    const Qji = Vi * Vj * (y_real * Math.sin(-dij) - y_imag * Math.cos(-dij));
    
    const baseMVA = system.baseMVA || 100;
    const loading = Math.sqrt(Pij * Pij + Qij * Qij) / line.rating * 100;
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Pij * baseMVA,
      qFrom: Qij * baseMVA,
      pTo: Pji * baseMVA,
      qTo: Qji * baseMVA,
      ploss: (Pij + Pji) * baseMVA,
      qloss: (Qij + Qji) * baseMVA,
      loading
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
 * Per §4A contract
 */
export function solveNewtonRaphson(
  system: PowerSystem, 
  tolerance = 1e-8, 
  maxIterations = 100
): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Initialize voltages
  const V: number[] = new Array(n);
  const theta: number[] = new Array(n);
  let slackIdx = -1;
  let pvBuses: number[] = [];
  let pqBuses: number[] = [];

  system.buses.forEach((bus, idx) => {
    V[idx] = bus.voltage || 1.0;
    theta[idx] = (bus.angle || 0) * Math.PI / 180;
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

  // Non-slack buses for state vector
  const nonSlackBuses: number[] = [];
  for (let i = 0; i < n; i++) {
    if (i !== slackIdx) nonSlackBuses.push(i);
  }
  const np = nonSlackBuses.length;

  let converged = false;
  let iterations = 0;
  let maxMismatch = Infinity;

  while (!converged && iterations < maxIterations) {
    // Calculate power injections: P_i = V_i * Σ_j V_j * (G_ij * cos θ_ij + B_ij * sin θ_ij)
    const Pcalc: number[] = new Array(n).fill(0);
    const Qcalc: number[] = new Array(n).fill(0);

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const Vi = V[i];
        const Vj = V[j];
        const theta_ij = theta[i] - theta[j];
        const cos_ij = Math.cos(theta_ij);
        const sin_ij = Math.sin(theta_ij);
        
        Pcalc[i] += Vi * Vj * (ybus.g[i][j] * cos_ij + ybus.b[i][j] * sin_ij);
        Qcalc[i] += Vi * Vj * (ybus.g[i][j] * sin_ij - ybus.b[i][j] * cos_ij);
      }
    }

    // Build mismatch vector
    const mismatches: number[] = [];
    for (const i of nonSlackBuses) {
      mismatches.push(P[i] - Pcalc[i]);
    }
    for (const i of pqBuses) {
      mismatches.push(Q[i] - Qcalc[i]);
    }

    // Calculate max mismatch
    maxMismatch = 0;
    for (const m of mismatches) {
      maxMismatch = Math.max(maxMismatch, Math.abs(m));
    }

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    // Build Jacobian
    const nn = mismatches.length; // np + nPQ
    const J: number[][] = new Array(nn).fill(null).map(() => new Array(nn).fill(0));

    // J1: dP/dθ for non-slack buses
    for (let p = 0; p < np; p++) {
      const i = nonSlackBuses[p];
      for (let q = 0; q < np; q++) {
        const j = nonSlackBuses[q];
        if (i === j) {
          // Diagonal: J1[p,p] = -Q_i - B_ii * V_i²
          let sum = 0;
          for (let k = 0; k < n; k++) {
            sum += V[i] * V[k] * (ybus.g[i][k] * Math.sin(theta[i] - theta[k]) - ybus.b[i][k] * Math.cos(theta[i] - theta[k]));
          }
          J[p][q] = -Qcalc[i] - ybus.b[i][i] * V[i] * V[i];
        } else {
          // Off-diagonal: J1[p,q] = V_i * V_j * (G_ij * sin θ_ij - B_ij * cos θ_ij)
          J[p][q] = V[i] * V[j] * (ybus.g[i][j] * Math.sin(theta[i] - theta[j]) - ybus.b[i][j] * Math.cos(theta[i] - theta[j]));
        }
      }
    }

    // J2: dP/dV for non-slack buses
    for (let p = 0; p < np; p++) {
      const i = nonSlackBuses[p];
      for (let q = 0; q < pqBuses.length; q++) {
        const j = pqBuses[q];
        // J2[p,q] = V_i * (G_ij * cos θ_ij + B_ij * sin θ_ij)
        J[p][np + q] = V[i] * (ybus.g[i][j] * Math.cos(theta[i] - theta[j]) + ybus.b[i][j] * Math.sin(theta[i] - theta[j]));
      }
    }

    // J3: dQ/dθ for PQ buses
    for (let p = 0; p < pqBuses.length; p++) {
      const i = pqBuses[p];
      for (let q = 0; q < np; q++) {
        const j = nonSlackBuses[q];
        // J3[p,q] = -V_i * V_j * (G_ij * cos θ_ij + B_ij * sin θ_ij)
        J[np + p][q] = -V[i] * V[j] * (ybus.g[i][j] * Math.cos(theta[i] - theta[j]) + ybus.b[i][j] * Math.sin(theta[i] - theta[j]));
      }
    }

    // J4: dQ/dV for PQ buses
    for (let p = 0; p < pqBuses.length; p++) {
      const i = pqBuses[p];
      for (let q = 0; q < pqBuses.length; q++) {
        const j = pqBuses[q];
        if (i === j) {
          // Diagonal: J4[p,p] = (Q_i - B_ii * V_i²) / V_i
          J[np + p][np + q] = (Qcalc[i] - ybus.b[i][i] * V[i] * V[i]) / V[i];
        } else {
          // Off-diagonal: J4[p,q] = V_i * (G_ij * sin θ_ij - B_ij * cos θ_ij)
          J[np + p][np + q] = V[i] * (ybus.g[i][j] * Math.sin(theta[i] - theta[j]) - ybus.b[i][j] * Math.cos(theta[i] - theta[j]));
        }
      }
    }

    // Solve for state update
    const dx = solveLinearSystem(J, mismatches);

    // Update state: θ for non-slack, V for PQ buses
    for (let p = 0; p < np; p++) {
      theta[nonSlackBuses[p]] += dx[p];
    }
    for (let p = 0; p < pqBuses.length; p++) {
      V[pqBuses[p]] += dx[np + p];
      V[pqBuses[p]] = Math.max(0.5, Math.min(1.5, V[pqBuses[p]]));
    }

    // Restore PV bus voltages
    for (const i of pvBuses) {
      V[i] = system.buses[i].voltage || 1.05;
    }

    iterations++;
  }

  // Calculate line flows
  const baseMVA = system.baseMVA || 100;
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const Vi = V[i];
    const Vj = V[j];
    const dij = theta[i] - theta[j];
    const cos_ij = Math.cos(dij);
    const sin_ij = Math.sin(dij);
    
    // Use YBus admittance
    const gij = ybus.g[i][j];
    const bij = ybus.b[i][j];
    
    // P + jQ at bus i (from end)
    const Pij = Vi * Vj * (gij * cos_ij + bij * sin_ij);
    const Qij = Vi * Vj * (gij * sin_ij - bij * cos_ij);
    
    // P + jQ at bus j (to end)
    const Pji = Vi * Vj * (gij * cos_ij - bij * sin_ij);
    const Qji = -Vi * Vj * (gij * sin_ij + bij * cos_ij);
    
    const loading = Math.sqrt(Pij * Pij + Qij * Qij) / line.rating * 100;
    
    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Pij * baseMVA,
      qFrom: Qij * baseMVA,
      pTo: Pji * baseMVA,
      qTo: Qji * baseMVA,
      ploss: (Pij + Pji) * baseMVA,
      qloss: (Qij + Qji) * baseMVA,
      loading
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
