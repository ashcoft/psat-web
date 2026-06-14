# Module: psat.packages.fcclassclass.remove
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
a.n = a.n - len(idx)
a.Ik(idx) = []
a.Vk(idx) = []
a.pH2(idx) = []
a.pH2O(idx) = []
a.pO2(idx) = []
a.qH2(idx) = []
a.m(idx) = []
a.u(idx) = []