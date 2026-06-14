# Module: psat.packages.ltclassclass.gettrace
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function traceY = gettrace(a,traceY)

if not a.n, return, end

idx = find(a.u)

if not isempty(idx)
  traceY(a.bus1(idx)) = 1
  traceY(a.bus2(idx)) = 1