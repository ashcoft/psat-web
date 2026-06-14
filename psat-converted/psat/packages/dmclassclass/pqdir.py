# Module: psat.packages.dmclassclass.pqdir
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [p,q] = pqdir(a,idx)

p = 0
q = 0

if not a.n, return, end

if not isempty(idx)
  p = sum(a.u(idx).*a.con(idx,3))
  q = sum(a.u(idx).*a.con(idx,4))