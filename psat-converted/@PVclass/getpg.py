# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\getpg.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = getpg(a,idx)

p = 0
if not a.n, return, end
if isempty(idx), return, end
if isnumeric(idx)
  p = a.u(idx).*a.con(idx,4)
elseif strcmp(idx,'all')
  p = a.u.*a.con(:,4)
