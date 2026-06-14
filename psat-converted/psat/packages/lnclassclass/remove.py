# Module: psat.packages.lnclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.fr(idx) = []
a.to(idx) = []
a.vfr(idx) = []
a.vto(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)