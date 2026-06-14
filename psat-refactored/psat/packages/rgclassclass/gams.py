# Module: psat.packages.rgclassclass.gams
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function data = gams(a,data,sdx)

if not a.n, return, end

idx = find(a.u)

if not isempty(idx)
  data(a.sup(idx),sdx) = a.con(idx,[9,5,6,3,4,7,8])