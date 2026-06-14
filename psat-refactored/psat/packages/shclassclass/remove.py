# Module: psat.packages.shclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if isempty(idx), return, end

a.n = a.n - len(idx)
a.con(idx,:) = []
a.bus(idx) = []
a.vbus(idx) = []
a.u(idx) = []