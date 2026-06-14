# Module: psat.packages.pvclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,k)

global DAE

if not a.n, return, end

if isempty(k), return, end
if not isempty(DAE.Gk)
  DAE.Gk(a.bus(k)) = 0
a.con(k,:) = []
a.bus(k) = []
a.vbus(k) = []
a.u(k) = []
a.pq(k) = []
a.qg(k) = []
a.n = a.n - len(k)
a.qmax(k) = []
a.qmin(k) = []