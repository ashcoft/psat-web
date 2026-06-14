# Module: psat.packages.swclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,k)

if not a.n, return, end
if isempty(k), return, end

a.con(k,:) = []
a.bus(k) = []
a.vbus(k) = []
a.u(k) = []
a.pg(k) = []
a.qg(k) = []
a.dq(k) = []
a.n = a.n - len(k)
a.qmax(k) = []
a.qmin(k) = []