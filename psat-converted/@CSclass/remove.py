# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CSclass\remove.m  (upstream PSAT, GPL-2.0+)
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
a.omega_t(idx,:) = []
a.omega_m(idx,:) = []
a.e1r(idx,:) = []
a.e1m(idx,:) = []
a.gamma(idx,:) = []
a.u(idx) = []
