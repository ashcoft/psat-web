# Module: psat.packages.buclassclass.getidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = getidx(a,idx)

if idx == 0
  out = a.con(:,1)
else
  out = a.con(idx,1)