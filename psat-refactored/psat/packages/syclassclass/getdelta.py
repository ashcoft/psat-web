# Module: psat.packages.syclassclass.getdelta
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function delta = getdelta(a)

global DAE

delta = []

if not a.n, return, end

delta = a.u.*DAE.x(a.delta)