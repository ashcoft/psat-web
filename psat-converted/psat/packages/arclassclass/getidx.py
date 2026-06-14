# Module: psat.packages.arclassclass.getidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function values = getidx(a,idx)

if not a.n, return, end

if isempty(idx)
  values = []
elseif idx(1) == 0
  values = a.con(:,1)
else
  values = a.con(idx,1)