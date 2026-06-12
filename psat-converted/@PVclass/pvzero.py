# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\pvzero.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pvzero(a,idx)

if not a.n, return, end
if isnumeric(idx)
  a.con(idx,4) = 0
elseif strcmp(idx,'all')
  a.con(:,4) = 0
