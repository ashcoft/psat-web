# Module: psat.packages.dmclassclass.pset
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pset(a,p)

if not a.n, return, end
if isempty(p), return, end
a.con(:,7) = p