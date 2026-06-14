# Module: psat.packages.dfclassclass.remove
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
a.wind(idx) = []
a.n = a.n - len(idx)
a.omega_m(idx) = []
a.theta_p(idx) = []
a.idr(idx) = []
a.iqr(idx) = []
a.vref(idx) = []
a.pwa(idx) = []
a.u(idx) = []