# Module: psat.packages.lnclassclass.diagy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function YBB = diagy(a)

YBB = []

if not a.n, return, end

r = a.con(:,8)
x = a.con(:,9)
z = r + i*x
y = a.u./z
YBB = diag(y)