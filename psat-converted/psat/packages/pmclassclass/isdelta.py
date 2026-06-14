# Module: psat.packages.pmclassclass.isdelta
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = isdelta(a,idx)

global Settings

out = 0

if not a.n, return, end

if Settings.hostver > 7
  out = not isempty(find(a.u.*a.thetam == idx,1))
else
  out = not isempty(find(a.u.*a.thetam == idx))