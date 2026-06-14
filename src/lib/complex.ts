export interface Complex { real: number; imag: number }

export const complex = (real: number, imag: number = 0): Complex => ({ real, imag });
export const cAdd = (a: Complex, b: Complex): Complex => ({ real: a.real + b.real, imag: a.imag + b.imag });
export const cSub = (a: Complex, b: Complex): Complex => ({ real: a.real - b.real, imag: a.imag - b.imag });
export const cMul = (a: Complex, b: Complex): Complex => ({ real: a.real * b.real - a.imag * b.imag, imag: a.real * b.imag + a.imag * b.real });
export const cConj = (a: Complex): Complex => ({ real: a.real, imag: -a.imag });
export const cAbs = (a: Complex): number => Math.sqrt(a.real * a.real + a.imag * a.imag);
export const cPolar = (mag: number, ang: number): Complex => ({ real: mag * Math.cos(ang), imag: mag * Math.sin(ang) });
export const cAngle = (a: Complex): number => Math.atan2(a.imag, a.real);
export const cDeg = (a: Complex): number => cAngle(a) * 180 / Math.PI;
