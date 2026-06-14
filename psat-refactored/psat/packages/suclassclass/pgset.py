# Module: psat.packages.suclassclass.pgset
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pgset(a)

if not a.n, return, end
a.con(:,3) = a.u.*a.con(:,6)