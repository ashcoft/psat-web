# Module: psat.packages.pqclassclass.pqactual
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pqactual(a,idx)

if not a.n, return, end
if isnumeric(idx)
  a.P0(idx) = a.u(idx).*a.con(idx,4)
  a.Q0(idx) = a.u(idx).*a.con(idx,5)
elseif strcmp(idx,'all')
  a.P0 = a.u.*a.con(:,4)
  a.Q0 = a.u.*a.con(:,5)