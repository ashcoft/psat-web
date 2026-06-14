export function cloneMatrix(a: number[][]): number[][] {
  return a.map(row => [...row]);
}

export function transpose(a: number[][]): number[][] {
  const m = a.length, n = a[0].length;
  const t: number[][] = Array.from({ length: n }, () => new Array(m).fill(0));
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      t[j][i] = a[i][j];
  return t;
}

export function matMul(a: number[][], b: number[][]): number[][] {
  const m = a.length, n = a[0].length, p = b[0].length;
  const r: number[][] = Array.from({ length: m }, () => new Array(p).fill(0));
  for (let i = 0; i < m; i++)
    for (let k = 0; k < n; k++)
      if (a[i][k] !== 0)
        for (let j = 0; j < p; j++)
          r[i][j] += a[i][k] * b[k][j];
  return r;
}

export function matVecMul(a: number[][], x: number[]): number[] {
  const m = a.length, n = a[0].length;
  const r = new Array(m).fill(0);
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      r[i] += a[i][j] * x[j];
  return r;
}

export function identity(n: number): number[][] {
  const I: number[][] = Array.from({ length: n }, () => new Array(n).fill(0));
  for (let i = 0; i < n; i++) I[i][i] = 1;
  return I;
}

export function solveLU(A: number[][], b: number[]): number[] {
  const n = A.length;
  const LU = cloneMatrix(A);
  const piv = new Array(n).fill(0).map((_, i) => i);

  for (let k = 0; k < n; k++) {
    let maxVal = Math.abs(LU[k][k]), maxRow = k;
    for (let i = k + 1; i < n; i++) {
      if (Math.abs(LU[i][k]) > maxVal) {
        maxVal = Math.abs(LU[i][k]);
        maxRow = i;
      }
    }
    if (maxVal < 1e-15) throw new Error('Singular matrix');
    if (maxRow !== k) {
      [LU[k], LU[maxRow]] = [LU[maxRow], LU[k]];
      [piv[k], piv[maxRow]] = [piv[maxRow], piv[k]];
    }
    for (let i = k + 1; i < n; i++) {
      LU[i][k] /= LU[k][k];
      for (let j = k + 1; j < n; j++)
        LU[i][j] -= LU[i][k] * LU[k][j];
    }
  }

  let x = [...b];
  for (let i = 0; i < n; i++) {
    if (piv[i] !== i) {
      [x[i], x[piv[i]]] = [x[piv[i]], x[i]];
    }
  }
  for (let i = 0; i < n; i++) {
    let sum = 0;
    for (let j = 0; j < i; j++) sum += LU[i][j] * x[j];
    x[i] -= sum;
  }
  for (let i = n - 1; i >= 0; i--) {
    let sum = 0;
    for (let j = i + 1; j < n; j++) sum += LU[i][j] * x[j];
    x[i] = (x[i] - sum) / LU[i][i];
  }
  return x;
}

export function solveGauss(A: number[][], b: number[]): number[] {
  return solveLU(A, b);
}

export function matInv(A: number[][]): number[][] {
  const n = A.length;
  const I = identity(n);
  return I.map((col) => solveLU(A, col));
}

function hypotArray(arr: number[]): number {
  return Math.sqrt(arr.reduce((s, v) => s + v * v, 0));
}

function sign(a: number): number {
  return a >= 0 ? 1 : -1;
}

export function qrAlgorithm(A: number[][], maxIter: number = 500, tol: number = 1e-12): { real: number[]; imag: number[] } {
  const n = A.length;
  let T = cloneMatrix(A);
  const real: number[] = [];
  const imag: number[] = [];

  for (let iter = 0; iter < maxIter; iter++) {
    let converged = true;
    for (let i = n - 1; i >= 0; i--) {
      if (i === 0) continue;
      const s = Math.abs(T[i][i - 1]);
      if (s > tol * (Math.abs(T[i][i]) + Math.abs(T[i - 1][i - 1]))) {
        converged = false;
        break;
      }
    }
    if (converged) {
      for (let i = 0; i < n; i++) {
        real.push(T[i][i]);
        imag.push(0);
      }
      return { real, imag };
    }

    const shift = T[n - 1][n - 1];

    for (let i = 0; i < n; i++) T[i][i] -= shift;

    const [Q, R] = householderQR(T);

    T = matMul(R, Q);
    for (let i = 0; i < n; i++) T[i][i] += shift;

    for (let i = 0; i < n - 1; i++) {
      if (Math.abs(T[i + 1][i]) < tol) T[i + 1][i] = 0;
    }
  }

  for (let i = 0; i < n; i++) {
    if (i < n - 1 && Math.abs(T[i + 1][i]) > 1e-10) {
      const a = T[i][i], b = T[i][i + 1];
      const c = T[i + 1][i], d = T[i + 1][i + 1];
      const tr = a + d;
      const det = a * d - b * c;
      const disc = tr * tr - 4 * det;
      if (disc >= 0) {
        real.push((tr + Math.sqrt(disc)) / 2);
        imag.push(0);
        real.push((tr - Math.sqrt(disc)) / 2);
        imag.push(0);
      } else {
        real.push(tr / 2);
        imag.push(Math.sqrt(-disc) / 2);
        real.push(tr / 2);
        imag.push(-Math.sqrt(-disc) / 2);
      }
      i++;
    } else {
      real.push(T[i][i]);
      imag.push(0);
    }
  }

  return { real, imag };
}

function householderQR(A: number[][]): [number[][], number[][]] {
  const m = A.length, n = A[0].length;
  const Q = identity(m);
  const R = cloneMatrix(A);

  for (let k = 0; k < n; k++) {
    let x = new Array(m - k).fill(0);
    for (let i = k; i < m; i++) x[i - k] = R[i][k];

    const normX = hypotArray(x);
    if (normX === 0) continue;

    const alpha = -sign(x[0]) * normX;
    const u = x.map((v, i) => i === 0 ? v - alpha : v);
    const normU = hypotArray(u);
    if (normU === 0) continue;
    const v = u.map(ui => ui / normU);

    for (let j = k; j < n; j++) {
      let dot = 0;
      for (let i = k; i < m; i++) dot += v[i - k] * R[i][j];
      for (let i = k; i < m; i++) R[i][j] -= 2 * v[i - k] * dot;
    }

    for (let j = 0; j < m; j++) {
      let dot = 0;
      for (let i = k; i < m; i++) dot += v[i - k] * Q[i][j];
      for (let i = k; i < m; i++) Q[i][j] -= 2 * v[i - k] * dot;
    }
  }

  return [Q, R];
}

export function powerIteration(A: number[][], maxIter: number = 100, tol: number = 1e-10): { eigenvalue: number; eigenvector: number[] } {
  const n = A.length;
  let v = new Array(n).fill(0).map(() => Math.random() - 0.5);
  let eigenvalue = 0;

  for (let iter = 0; iter < maxIter; iter++) {
    const w = matVecMul(A, v);
    let norm = Math.sqrt(w.reduce((s, x) => s + x * x, 0));
    if (norm === 0) break;
    v = w.map(x => x / norm);
    const newEig = matVecMul(transpose(A), v).reduce((s, x, i) => s + x * v[i], 0);
    if (Math.abs(newEig - eigenvalue) < tol) {
      eigenvalue = newEig;
      break;
    }
    eigenvalue = newEig;
  }

  return { eigenvalue, eigenvector: v };
}

export function rayleighQuotient(A: number[][], v: number[]): number {
  const Av = matVecMul(A, v);
  const vTv = v.reduce((s, x) => s + x * x, 0);
  const vTAv = v.reduce((s, x, i) => s + x * Av[i], 0);
  return vTAv / vTv;
}

export function matrixFromArray(n: number, fn: (i: number, j: number) => number): number[][] {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => fn(i, j))
  );
}

export function vectorNorm(v: number[]): number {
  return Math.sqrt(v.reduce((s, x) => s + x * x, 0));
}

export function inPlaceReshape<T>(src: T[], nRows: number, nCols: number): T[][] {
  const r: T[][] = [];
  for (let i = 0; i < nRows; i++)
    r.push(src.slice(i * nCols, (i + 1) * nCols));
  return r;
}
