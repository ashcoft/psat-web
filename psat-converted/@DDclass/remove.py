# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DDclass\remove.m  (upstream PSAT, GPL-2.0+)
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
a.omega_m(idx,:) = []
a.theta_p(idx,:) = []
a.pwa(idx,:) = []
a.ids(idx,:) = []
a.iqs(idx,:) = []
a.idc(idx,:) = []
a.iqc(idx,:) = []
a.u(idx) = []
