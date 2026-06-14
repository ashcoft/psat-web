# Module: psat.packages.ciclassclass.isdelta
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = isdelta(a,idx)

global DAE Settings

out = 0

if not a.n, return, end

if Settings.hostver > 7
  out = not isempty(find((DAE.n+a.delta) == idx,1))
else
  out = not isempty(find((DAE.n+a.delta) == idx))