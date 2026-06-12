# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\pqreset.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pqreset(a,idx)

if not a.n, return, end
if isnumeric(idx)
  a.con(idx,4) = a.P0(idx)
  a.con(idx,5) = a.Q0(idx)
elseif strcmp(idx,'all')
  a.con(:,4) = a.P0
  a.con(:,5) = a.Q0
