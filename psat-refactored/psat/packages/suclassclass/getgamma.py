# Module: psat.packages.suclassclass.getgamma
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function gamma = getgamma(a)

gamma = []

if not a.n, return, end

gamma = a.u.*a.con(:,15)