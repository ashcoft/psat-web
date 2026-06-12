# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@IMclass\remove.m  (upstream PSAT, GPL-2.0+)
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
a.slip(idx) = []
a.e1r(idx) = []
a.e1m(idx) = []
a.e2r(idx) = []
a.e2m(idx) = []
a.u(idx) = []
a.z(idx) = []
a.dat(idx,:) = []
