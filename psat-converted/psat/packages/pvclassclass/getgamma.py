# Module: psat.packages.pvclassclass.getgamma
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function gamma = getgamma(a)

gamma = 0
if not a.n, return, end

gamma = sum(a.u.*a.con(:,10))