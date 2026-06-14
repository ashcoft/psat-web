# Module: psat.packages.bfclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.bus(idx) = []
a.dat(idx) = []
a.n = a.n - len(idx)
a.x(idx,:) = []
a.w(idx,:) = []
a.u(idx) = []