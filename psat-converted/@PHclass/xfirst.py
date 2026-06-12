# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PHclass\xfirst.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def xfirst(a):

global DAE

if not a.n, return, end

DAE.x(a.alpha) = 0
DAE.x(a.Pm) = 0
idx = find(not a.con(:,7))
if not isempty(idx)
  warn(a,idx,'Measurement time constant Tm cannot be 0. Tm = 1e-3 will be used.')
  a.con(idx,7) = 1e-3

