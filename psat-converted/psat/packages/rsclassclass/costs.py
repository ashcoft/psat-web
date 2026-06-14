# Module: psat.packages.rsclassclass.costs
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function Cr = costs(a)

Cr = []

if not a.n, return, end

Cr = a.u.*a.con(:,5)