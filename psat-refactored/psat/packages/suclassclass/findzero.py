# Module: psat.packages.suclassclass.findzero
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = findzero(a)

idx = []
if not a.n, return, end
idx = find(a.u.*a.con(:,3) == 0)