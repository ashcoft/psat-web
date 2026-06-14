# Module: psat.packages.swclassclass.swsum
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = swsum(a,idx,p)

if not a.n, return, end
if isempty(idx), return, end
a.pg(idx) = a.u(idx).*(a.pg(idx) + p)