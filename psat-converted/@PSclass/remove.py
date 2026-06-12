# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PSclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.bus(idx) = []
a.vbus(idx) = []
a.exc(idx) = []
a.syn(idx) = []
a.va(idx) = []
a.v1(idx) = []
a.v2(idx) = []
a.v3(idx) = []
a.vss(idx) = []
a.u(idx) = []
a.s1(idx) = []
a.omega(idx) = []
a.p(idx) = []
a.vf(idx) = []
a.vref(idx) = []
a.n = a.n - len(idx)
