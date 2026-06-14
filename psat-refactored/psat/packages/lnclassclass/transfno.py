# Module: psat.packages.lnclassclass.transfno
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function n = transfno(a)

n = 0

if not a.n, return, end

n = len(find(a.con(:,7) != 0))
