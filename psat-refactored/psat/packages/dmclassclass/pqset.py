# Module: psat.packages.dmclassclass.pqset
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pqset(a,tanphi)

if not a.n, return, end
a.con(:,3) = a.u.*a.con(:,7)
a.con(:,4) = a.u.*a.con(:,7).*tanphi