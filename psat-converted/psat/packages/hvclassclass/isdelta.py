# Module: psat.packages.hvclassclass.isdelta
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
  out1 = not isempty(find((DAE.n + a.u.*a.phir) == idx,1))
  out2 = not isempty(find((DAE.n + a.u.*a.phii) == idx,1))
else
  out1 = not isempty(find((DAE.n + a.u.*a.phir) == idx))
  out2 = not isempty(find((DAE.n + a.u.*a.phii) == idx))

out = out1  or  out2