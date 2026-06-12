# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@RGclass\gams.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function data = gams(a,data,sdx)

if not a.n, return, end

idx = find(a.u)

if not isempty(idx)
  data(a.sup(idx),sdx) = a.con(idx,[9,5,6,3,4,7,8])
