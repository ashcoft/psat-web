# Module: psat.packages.swclassclass.getpg
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = getpg(a,idx)

p = 0
if not a.n, return, end
if isempty(idx), return, end
if isnumeric(idx)
  p = a.pg(idx(find(a.u(idx))))
elseif strcmp(idx,'all')
  p = a.pg(find(a.u))