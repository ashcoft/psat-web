# Module: psat.packages.pvclassclass.pvmul
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pvmul(a,idx,k)

if not a.n, return, end

if isnumeric(idx)
  a.con(idx,4) = k*a.con(idx,4)
elseif strcmp(idx,'all')
  a.con(:,4) = k*a.con(:,4)