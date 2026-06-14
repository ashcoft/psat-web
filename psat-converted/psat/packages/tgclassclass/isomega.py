# Module: psat.packages.tgclassclass.isomega
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = isomega(a,idx)

global Settings DAE

out = 0

if not a.n, return, end

if Settings.hostver > 7
  out = not isempty(find((DAE.n+a.wref) == idx,1))
else
  out = not isempty(find((DAE.n+a.wref) == idx))
