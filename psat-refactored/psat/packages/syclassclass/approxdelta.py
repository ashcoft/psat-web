# Module: psat.packages.syclassclass.approxdelta
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function delta = approxdelta(a)

global DAE

delta = a.u.*(DAE.x(a.delta)-a.con(:,9).*DAE.y(a.pm))