# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\setpg.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setpg(a,idx,p)

if not a.n, return, end
if isempty(idx), return, end
if isnumeric(idx)
  jdx = idx(find(a.u(idx)))
elseif strcmp(idx,'all')
  jdx = find(a.u)

a.pg(jdx) = a.u(jdx).*p(jdx)
#a.store(jdx,10) = a.pg(jdx);
