# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\swgamma.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function y = swgamma(a,idx)

y = 0
if not a.n, return, end
if isnumeric(idx)
  y = a.u(idx).*a.con(idx,11)
elseif strcmp(idx,'sum')
  y = a.u.*sum(a.con(:,11))
