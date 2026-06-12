# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.q(idx) = []
a.cac(idx) = []
a.exc(idx) = []
a.syn(idx) = []
a.svc(idx) = []
a.vref(idx) = []
a.dVsdQ(idx) = []
a.Vs(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)
