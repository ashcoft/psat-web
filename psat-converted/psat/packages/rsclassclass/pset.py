# Module: psat.packages.rsclassclass.pset
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pset(a,Pr)

if not a.n, return, end

a.Pr = Pr
