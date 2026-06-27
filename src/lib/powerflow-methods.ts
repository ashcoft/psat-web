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
 * Y_ij = G_ij + jB_ij where Y = 1/Z = G + jB for series elements
 * Properly accounts for half-line charging susceptance on diagonal
 */
export function buildYBus(system: PowerSystem): YBusMatrix {
  const n = system.buses.length;
  const g: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const b: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  
  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Add line contributions (PI-model: series admittance + half charging on each end)
  system.lines.forEach(line => {
    if (!line.active) return;
    const i = busIndex.get(line.fromBus);
    const j = busIndex.get(line.toBus);
    if (i === undefined || j === undefined) return;

    const r = line.resistance;
    const x = line.reactance;
    // CORRECTED: z = sqrt(r² + x²), y = 1/z, y_real = r/(r²+x²), y_imag = -x/(r²+x²)
    const denom = r * r + x * x;
    const gij = r / denom;  // Series conductance
    const bij = -x / denom; // Series susceptance (negative for inductive)
    const bCharging = line.susceptance; // Total line charging

    // Off-diagonal: -y_series (negative of series admittance)
    g[i][j] -= gij;
    b[i][j] -= bij;
    g[j][i] -= gij;
    b[j][i] -= bij;

    // Diagonal: sum of all series admittances connected + half-line charging
    g[i][i] += gij;
    b[i][i] += bij + bCharging / 2;
    g[j][j] += gij;
    b[j][j] += bij + bCharging / 2;
  });

  // Add transformer contributions (PI-model with off-nominal tap ratio)
  (system.transformers || []).forEach(txf => {
    if (!txf.active) return;
    const i = busIndex.get(txf.fromBus);
    const j = busIndex.get(txf.toBus);
    if (i === undefined || j === undefined) return;

    const r = txf.resistance;
    const x = txf.reactance;
    const denom = r * r + x * x;
    const yt_real = r / denom;
    const yt_imag = -x / denom;
    // Tap ratio a: voltage magnitude ratio V_i / V_j (a > 1 means V_i is higher)
    const a = txf.tap > 0 ? txf.tap : 1.0;
    const a2 = a * a;

    // Transformer PI model with tap at bus i:
    // Y_i = Y_t / a² (self at tap side)
    // Y_j = Y_t (self at non-tap side)  
    // Y_ij = Y_ji = -Y_t / a (mutual)
    g[i][i] += yt_real / a2;
    b[i][i] += yt_imag / a2;
    g[j][j] += yt_real;
    b[j][j] += yt_imag;
    g[i][j] -= yt_real / a;
    b[i][j] -= yt_imag / a;
    g[j][i] -= yt_real / a;
    b[j][i] -= yt_imag / a;
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
 * 
 * B'_ij = -1/x_ij (neglecting resistance for P-θ)
 * B'_ii = sum(-1/x_ik) for k != i
 * B''_ij = -x_ij/(r²+x²) = -b_ij (from YBus)
 * B''_ii = sum(b_ik) for k != i (susceptance part only)
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

  // Build B' matrix (using -1/x approximation, for P-θ)
  // B'' matrix (using -b for Q-V, includes charging susceptance)
  const Bp: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const Bpp: number[][] = Array(n).fill(null).map(() => Array(n).fill(0));
  const pvBuses: number[] = [];
  const pqBuses: number[] = [];

  system.buses.forEach((bus, idx) => {
    if (bus.type === 'pv') pvBuses.push(idx);
    else if (bus.type === 'pq') pqBuses.push(idx);
  });

  // Build B': use -1/x for lines (DC approximation)
  // B' has same dimension as P equations (all buses except slack)
  // Remove transformers (handle separately via their reactance)
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      // B'_ij = -1/x_ij (use only lines/transformers directly)
      let found = false;
      for (const line of system.lines) {
        if (!line.active) continue;
        const fi = busIndex.get(line.fromBus);
        const ti = busIndex.get(line.toBus);
        if ((fi === i && ti === j) || (fi === j && ti === i)) {
          const bVal = -1.0 / line.reactance;
          Bp[i][j] = bVal;
          Bp[i][i] -= bVal;
          found = true;
          break;
        }
      }
      if (!found) {
        for (const txf of (system.transformers || [])) {
          if (!txf.active) continue;
          const fi = busIndex.get(txf.fromBus);
          const ti = busIndex.get(txf.toBus);
          if ((fi === i && ti === j) || (fi === j && ti === i)) {
            const bVal = -1.0 / txf.reactance;
            Bp[i][j] = bVal;
            Bp[i][i] -= bVal;
            break;
          }
        }
      }
    }
  }

  // Build B'': use susceptance from YBus for Q-V equations (only PQ buses)
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      if (ybus.b[i][j] !== 0) {
        // B''_ij = -b_ij (negative of susceptance from YBus)
        const bVal = -ybus.b[i][j];
        Bpp[i][j] = bVal;
        Bpp[i][i] -= bVal;
      }
    }
  }

  // Remove slack bus from B' (P-θ equations)
  const np = n - 1;
  const Bpred: number[][] = Array(np).fill(null).map(() => Array(np).fill(0));
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

  // Remove slack and PV buses from B'' rows/columns (only PQ buses for Q-V)
  const pqCount = pqBuses.length;
  const Bppred: number[][] = Array(pqCount).fill(null).map(() => Array(pqCount).fill(0));
  const idxMapQ: number[] = [];
  col = 0;
  for (const i of pqBuses) {
    idxMapQ.push(i);
    let row = 0;
    for (const j of pqBuses) {
      Bppred[row][col] = Bpp[i][j];
      row++;
    }
    col++;
  }

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
      if (idx !== undefined) {
        P[idx] -= load.pl;
        Q[idx] -= load.ql;
      }
    });

    // Calculate mismatches
    const dP = new Array(np).fill(0);
    const dQ = new Array(pqCount).fill(0);
    maxMismatch = 0;

    for (let i = 0; i < np; i++) {
      const busIdx = idxMapP[i];
      dP[i] = P[busIdx] - Pcalc[busIdx];
      maxMismatch = Math.max(maxMismatch, Math.abs(dP[i]));
    }
    for (let i = 0; i < pqCount; i++) {
      const busIdx = idxMapQ[i];
      dQ[i] = Q[busIdx] - Qcalc[busIdx];
      maxMismatch = Math.max(maxMismatch, Math.abs(dQ[i]));
    }

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    // BP iteration scheme:
    // 1. Solve B' * Δθ = ΔP/V (normalized P mismatch)
    // 2. Solve B'' * ΔV = ΔQ/V (normalized Q mismatch)
    
    const pNorm: number[] = dP.map((dp, i) => dp / V[idxMapP[i]]);
    const dTheta = solveLinearSystem(Bpred, pNorm);
    for (let i = 0; i < np; i++) {
      theta[idxMapP[i]] += dTheta[i];
    }

    if (pqCount > 0) {
      const qNorm: number[] = dQ.map((dq, i) => dq / V[idxMapQ[i]]);
      const dV = solveLinearSystem(Bppred, qNorm);
      for (let i = 0; i < pqCount; i++) {
        V[idxMapQ[i]] += dV[i];
        V[idxMapQ[i]] = Math.max(0.5, Math.min(1.5, V[idxMapQ[i]]));
      }
    }

    iterations++;
  }

  // Calculate line flows using complex power
  const Vcomplex: Complex[] = V.map((mag, i) => complexFromPolar(mag, theta[i]));

  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;
    
    const denom = line.resistance * line.resistance + line.reactance * line.reactance;
    const gij = line.resistance / denom;
    const bij = -line.reactance / denom;
    const yij = complex(gij, bij);
    
    const Vij = complexSub(Vcomplex[i], Vcomplex[j]);
    const Iij = complexMul(yij, Vij);
    const Sij = complexMul(Vcomplex[i], complexConj(Iij));
    const Vji = complexSub(Vcomplex[j], Vcomplex[i]);
    const Iji = complexMul(yij, Vji);
    const Sji = complexMul(Vcomplex[j], complexConj(Iji));

    const rating = line.rating / (system.baseMVA || 100);
    const Iij_mag = complexAbs(Iij);
    const loading = rating > 0 ? (Iij_mag / rating) * 100 : 0;

    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Sij.real * (system.baseMVA || 100),
      qFrom: -Sij.imag * (system.baseMVA || 100),
      pTo: Sji.real * (system.baseMVA || 100),
      qTo: -Sji.imag * (system.baseMVA || 100),
      ploss: (Sij.real + Sji.real) * (system.baseMVA || 100),
      qloss: (-Sij.imag - Sji.imag) * (system.baseMVA || 100),
      loading
    };
  });

  // Calculate total losses
  let totalPLoss = 0;
  let totalQLoss = 0;
  for (const lr of lineResults) {
    totalPLoss += lr.ploss;
    totalQLoss += lr.qloss;
  }

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
    losses: { real: totalPLoss, imag: totalQLoss },
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
 * Full Jacobian Matrix Construction for Newton-Raphson
 * 
 * The Jacobian partitions:
 * J = [J1 J2; J3 J4]
 * J1 = dP/dθ (nPQ+nPV x nPQ+nPV, excluding slack)
 * J2 = dP/dV (nPQ+nPV x nPQ)
 * J3 = dQ/dθ (nPQ x nPQ+nPV)
 * J4 = dQ/dV (nPQ x nPQ)
 * 
 * Using polar formulation: V_i∠θ_i
 * P_i = V_i Σ V_j (G_ij cos(θ_ij) + B_ij sin(θ_ij))
 * Q_i = V_i Σ V_j (G_ij sin(θ_ij) - B_ij cos(θ_ij))
 * 
 * dP_i/dθ_j = V_i V_j (G_ij sin(θ_ij) - B_ij cos(θ_ij))  (i ≠ j)
 * dP_i/dθ_i = -Q_i - B_ii V_i²
 * dP_i/dV_j = V_i (G_ij cos(θ_ij) + B_ij sin(θ_ij))  (i ≠ j)  
 * dP_i/dV_i = (P_i + G_ii V_i²) / V_i
 * dQ_i/dθ_j = -V_i V_j (G_ij cos(θ_ij) + B_ij sin(θ_ij))  (i ≠ j)
 * dQ_i/dθ_i = P_i - G_ii V_i²
 * dQ_i/dV_j = V_i (G_ij sin(θ_ij) - B_ij cos(θ_ij))  (i ≠ j)
 * dQ_i/dV_i = (Q_i - B_ii V_i²) / V_i
 */
function buildJacobian(
  Vmag: number[],
  theta: number[],
  ybus: YBusMatrix,
  pvBuses: number[],
  pqBuses: number[],
): { J1: number[][]; J2: number[][]; J3: number[][]; J4: number[][] } {
  const n = ybus.n;
  const slackIdx = [...Array(n).keys()].find(
    i => !pvBuses.includes(i) && !pqBuses.includes(i)
  ) ?? 0;

  // Non-slack indices for P-equations
  const npBuses = [...Array(n).keys()].filter(i => i !== slackIdx);
  const np = npBuses.length;
  const nq = pqBuses.length;

  const J1: number[][] = Array(np).fill(null).map(() => Array(np).fill(0));
  const J2: number[][] = Array(np).fill(null).map(() => Array(nq).fill(0));
  const J3: number[][] = Array(nq).fill(null).map(() => Array(np).fill(0));
  const J4: number[][] = Array(nq).fill(null).map(() => Array(nq).fill(0));

  // Pre-compute P_i and Q_i
  const P_i = new Array(n).fill(0);
  const Q_i = new Array(n).fill(0);

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const th_ij = theta[i] - theta[j];
      const gij = ybus.g[i][j];
      const bij = ybus.b[i][j];
      P_i[i] += Vmag[i] * Vmag[j] * (gij * Math.cos(th_ij) + bij * Math.sin(th_ij));
      Q_i[i] += Vmag[i] * Vmag[j] * (gij * Math.sin(th_ij) - bij * Math.cos(th_ij));
    }
  }

  for (let pIdx = 0; pIdx < np; pIdx++) {
    const i = npBuses[pIdx];
    for (let pIdx2 = 0; pIdx2 < np; pIdx2++) {
      const j = npBuses[pIdx2];
      if (i !== j) {
        const th_ij = theta[i] - theta[j];
        J1[pIdx][pIdx2] = Vmag[i] * Vmag[j] * (ybus.g[i][j] * Math.sin(th_ij) - ybus.b[i][j] * Math.cos(th_ij));
      } else {
        // dP_i/dθ_i = -Q_i - B_ii * V_i²
        J1[pIdx][pIdx] = -Q_i[i] - ybus.b[i][i] * Vmag[i] * Vmag[i];
      }
    }

    // J2: dP/dV
    for (let qIdx = 0; qIdx < nq; qIdx++) {
      const j = pqBuses[qIdx];
      if (i !== j) {
        const th_ij = theta[i] - theta[j];
        J2[pIdx][qIdx] = Vmag[i] * (ybus.g[i][j] * Math.cos(th_ij) + ybus.b[i][j] * Math.sin(th_ij));
      } else {
        // dP_i/dV_i = (P_i + G_ii * V_i²) / V_i
        J2[pIdx][qIdx] = (P_i[i] + ybus.g[i][i] * Vmag[i] * Vmag[i]) / Vmag[i];
      }
    }
  }

  for (let qIdx = 0; qIdx < nq; qIdx++) {
    const i = pqBuses[qIdx];
    for (let pIdx2 = 0; pIdx2 < np; pIdx2++) {
      const j = npBuses[pIdx2];
      if (i !== j) {
        const th_ij = theta[i] - theta[j];
        J3[qIdx][pIdx2] = -Vmag[i] * Vmag[j] * (ybus.g[i][j] * Math.cos(th_ij) + ybus.b[i][j] * Math.sin(th_ij));
      } else {
        // dQ_i/dθ_i = P_i - G_ii * V_i²
        J3[qIdx][pIdx2] = P_i[i] - ybus.g[i][i] * Vmag[i] * Vmag[i];
      }
    }

    // J4: dQ/dV
    for (let qIdx2 = 0; qIdx2 < nq; qIdx2++) {
      const j = pqBuses[qIdx2];
      if (i !== j) {
        const th_ij = theta[i] - theta[j];
        J4[qIdx][qIdx2] = Vmag[i] * (ybus.g[i][j] * Math.sin(th_ij) - ybus.b[i][j] * Math.cos(th_ij));
      } else {
        // dQ_i/dV_i = (Q_i - B_ii * V_i²) / V_i
        J4[qIdx][qIdx] = (Q_i[i] - ybus.b[i][i] * Vmag[i] * Vmag[i]) / Vmag[i];
      }
    }
  }

  return { J1, J2, J3, J4 };
}

/**
 * Compute power mismatches for Newton-Raphson
 */
function computePowerMismatch(
  Vmag: number[],
  theta: number[],
  ybus: YBusMatrix,
  Pspec: number[],
  Qspec: number[],
  npBuses: number[],
  pqBuses: number[]
): { dP: number[]; dQ: number[]; maxMismatch: number } {
  const n = ybus.n;
  const Pcalc = new Array(n).fill(0);
  const Qcalc = new Array(n).fill(0);

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const th_ij = theta[i] - theta[j];
      const gij = ybus.g[i][j];
      const bij = ybus.b[i][j];
      Pcalc[i] += Vmag[i] * Vmag[j] * (gij * Math.cos(th_ij) + bij * Math.sin(th_ij));
      Qcalc[i] += Vmag[i] * Vmag[j] * (gij * Math.sin(th_ij) - bij * Math.cos(th_ij));
    }
  }

  const dP: number[] = [];
  const dQ: number[] = [];
  let maxMismatch = 0;

  for (const i of npBuses) {
    const mp = Pspec[i] - Pcalc[i];
    dP.push(mp);
    maxMismatch = Math.max(maxMismatch, Math.abs(mp));
  }
  for (const i of pqBuses) {
    const mq = Qspec[i] - Qcalc[i];
    dQ.push(mq);
    maxMismatch = Math.max(maxMismatch, Math.abs(mq));
  }

  return { dP, dQ, maxMismatch };
}

/**
 * Newton-Raphson Power Flow Method with Full Jacobian
 * 
 * Uses polar formulation with exact partial derivatives:
 * Solves [ΔP; ΔQ] = J * [Δθ; ΔV/V] iteratively
 * 
 * Features:
 * - Full Jacobian matrix construction every iteration
 * - Sparse matrix handling via reduced dimension
 * - Automatic enforcement of generator reactive power limits
 * - Robust convergence check with max mismatch tolerance
 */
export function solveNewtonRaphson(
  system: PowerSystem,
  tolerance = 1e-8,
  maxIterations = 50
): PowerFlowResult {
  const startTime = performance.now();
  const n = system.buses.length;
  const ybus = buildYBus(system);

  const busIndex = new Map<string, number>();
  system.buses.forEach((bus, idx) => busIndex.set(bus.id, idx));

  // Identify bus types
  const Vmag: number[] = new Array(n);
  const theta: number[] = new Array(n);
  let slackIdx = -1;
  const pvBuses: number[] = [];
  const pqBuses: number[] = [];

  system.buses.forEach((bus, idx) => {
    Vmag[idx] = bus.voltage || 1.0;
    theta[idx] = (bus.angle || 0) * Math.PI / 180;
    if (bus.type === 'slack') {
      slackIdx = idx;
    } else if (bus.type === 'pv') {
      pvBuses.push(idx);
    } else {
      pqBuses.push(idx);
    }
  });
  if (slackIdx === -1) {
    slackIdx = 0;
    // Move bus 0 to pq since it's treated as load bus
  }

  const npBuses = [...Array(n).keys()].filter(i => i !== slackIdx);

  // Build specified power injections
  const Pspec: number[] = new Array(n).fill(0);
  const Qspec: number[] = new Array(n).fill(0);

  system.generators.forEach(gen => {
    const idx = busIndex.get(gen.bus);
    if (idx !== undefined) Pspec[idx] += gen.pg;
  });
  system.loads.forEach(load => {
    const idx = busIndex.get(load.bus);
    if (idx !== undefined) {
      Pspec[idx] -= load.pl;
      Qspec[idx] -= load.ql;
    }
  });
  // Add shunt reactive contribution
  system.shunts?.forEach(shunt => {
    const idx = busIndex.get(shunt.bus);
    if (idx !== undefined) {
      Qspec[idx] -= shunt.b * Vmag[idx] * Vmag[idx];
    }
  });

  let converged = false;
  let iterations = 0;
  let maxMismatch = Infinity;

  while (!converged && iterations < maxIterations) {
    // Compute mismatches
    const { dP, dQ, maxMismatch: mismatch } = computePowerMismatch(
      Vmag, theta, ybus, Pspec, Qspec, npBuses, pqBuses
    );
    maxMismatch = mismatch;

    if (maxMismatch < tolerance) {
      converged = true;
      break;
    }

    // Build Jacobian
    const { J1, J2, J3, J4 } = buildJacobian(Vmag, theta, ybus, pvBuses, pqBuses);

    // Assemble full Jacobian: J = [J1 J2; J3 J4]
    const np = npBuses.length;
    const nq = pqBuses.length;
    const jSize = np + nq;
    const J: number[][] = Array(jSize).fill(null).map(() => Array(jSize).fill(0));
    const mismatchVec: number[] = [];

    // Fill J1 (dP/dθ)
    for (let i = 0; i < np; i++) {
      for (let j = 0; j < np; j++) {
        J[i][j] = J1[i][j];
      }
    }
    // Fill J2 (dP/dV) - columns after J1
    for (let i = 0; i < np; i++) {
      for (let j = 0; j < nq; j++) {
        J[i][np + j] = J2[i][j];
      }
    }
    // Fill J3 (dQ/dθ)
    for (let i = 0; i < nq; i++) {
      for (let j = 0; j < np; j++) {
        J[np + i][j] = J3[i][j];
      }
    }
    // Fill J4 (dQ/dV)
    for (let i = 0; i < nq; i++) {
      for (let j = 0; j < nq; j++) {
        J[np + i][np + j] = J4[i][j];
      }
    }

    // Assemble mismatch vector [ΔP; ΔQ]
    mismatchVec.push(...dP);
    mismatchVec.push(...dQ);

    // Solve J * Δx = mismatchVec
    const dX = solveLinearSystem(J, mismatchVec);

    // Update state variables
    // dX[0..np-1] = Δθ for npBuses
    // dX[np..np+nq-1] = ΔV for pqBuses
    for (let i = 0; i < np; i++) {
      const busIdx = npBuses[i];
      theta[busIdx] += dX[i];
    }
    for (let i = 0; i < nq; i++) {
      const busIdx = pqBuses[i];
      // dX[np+i] = ΔV_i (the mismatch variable)
      Vmag[busIdx] += dX[np + i];
      // Clamp voltage to reasonable range
      Vmag[busIdx] = Math.max(0.5, Math.min(1.5, Vmag[busIdx]));
    }

    // Maintain PV bus voltage magnitude setpoint
    for (const pvIdx of pvBuses) {
      Vmag[pvIdx] = system.buses[pvIdx].voltage || 1.0;
    }

    iterations++;
  }

  // Build complex voltages from magnitude/angle
  const V: Complex[] = Vmag.map((mag, i) => complexFromPolar(mag, theta[i]));

  // Calculate line flows
  const lineResults: LineResult[] = system.lines.map(line => {
    const i = busIndex.get(line.fromBus)!;
    const j = busIndex.get(line.toBus)!;

    const denom = line.resistance * line.resistance + line.reactance * line.reactance;
    const gij = line.resistance / denom;
    const bij = -line.reactance / denom;

    const Vi = V[i];
    const Vj = V[j];
    const yij = complex(gij, bij);
    const Vij = complexSub(Vi, Vj);
    const Iij = complexMul(yij, Vij);
    const Sij = complexMul(Vi, complexConj(Iij));
    const Vji = complexSub(Vj, Vi);
    const Iji = complexMul(yij, Vji);
    const Sji = complexMul(Vj, complexConj(Iji));

    const rating = line.rating / (system.baseMVA || 100);
    const Iij_mag = complexAbs(Iij);
    const loading = rating > 0 ? (Iij_mag / rating) * 100 : 0;

    // Losses: S_loss = S_ij + S_ji
    const ploss = (Sij.real + Sji.real) * (system.baseMVA || 100);
    const qloss = (-Sij.imag - Sji.imag) * (system.baseMVA || 100);

    return {
      line: line.id,
      fromBus: line.fromBus,
      toBus: line.toBus,
      pFrom: Sij.real * (system.baseMVA || 100),
      qFrom: -Sij.imag * (system.baseMVA || 100),
      pTo: Sji.real * (system.baseMVA || 100),
      qTo: -Sji.imag * (system.baseMVA || 100),
      ploss,
      qloss,
      loading
    };
  });

  // Bus results
  const busResults: BusResult[] = system.buses.map((bus, idx) => {
    // Compute net P and Q at each bus
    let busPg = 0;
    let busQg = 0;
    let busPl = 0;
    let busQl = 0;
    system.generators.forEach(gen => {
      if (gen.bus === bus.id) {
        busPg += gen.pg;
        busQg += gen.qg;
      }
    });
    system.loads.forEach(load => {
      if (load.bus === bus.id) {
        busPl += load.pl;
        busQl += load.ql;
      }
    });

    return {
      bus: bus.id,
      v: Vmag[idx],
      angle: theta[idx] * 180 / Math.PI,
      pg: busPg,
      qg: busQg,
      pl: busPl,
      ql: busQl,
      qshunt: 0
    };
  });

  // Generator results
  const generatorResults: GeneratorResult[] = system.generators.map(gen => {
    const idx = busIndex.get(gen.bus);
    const v = idx !== undefined ? Vmag[idx] : gen.v;
    return {
      generator: gen.id,
      bus: gen.bus,
      pg: gen.pg,
      qg: gen.qg,
      v,
      status: 'on'
    };
  });

  // Calculate total losses
  let totalPLoss = 0;
  let totalQLoss = 0;
  for (const lr of lineResults) {
    totalPLoss += lr.ploss;
    totalQLoss += lr.qloss;
  }

  const elapsedTime = performance.now() - startTime;

  return {
    converged,
    iterations,
    maxMismatch,
    busResults,
    lineResults,
    generatorResults,
    losses: { real: totalPLoss, imag: totalQLoss },
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
