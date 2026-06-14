# Module: psat.packages.stclassclass.remove
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
a.vbus(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)
a.ist(idx,:) = []
a.Vref(idx,:) = []
a.vref(idx,:) = []