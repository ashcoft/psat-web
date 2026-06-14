# Module: psat.packages.swclassclass.setgamma
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setgamma(a)

z = a.con(:,12)
a.u = a.con(:,a.ncol)

a.con(find(z & a.u),11) = 1