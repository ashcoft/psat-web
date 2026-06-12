# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\setx0.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global DAE Syn

if not a.n, return, end

for i in range(1, a.n+1):
  idx = a.syn{i}
  DAE.y(a.delta(i)) = sum(a.M(idx).*DAE.x(a.dgen(idx)))/a.Mtot(i)
DAE.y(a.omega) = 1

fm_print('Initialization of COI completed.')


