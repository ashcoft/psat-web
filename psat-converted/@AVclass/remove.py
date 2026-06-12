# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.bus(idx) = []
a.vbus(idx) = []
a.syn(idx) = []
a.vref(idx) = []
a.vref0(idx) = []
a.vr1(idx) = []
a.vr2(idx) = []
a.vr3(idx) = []
a.vfd(idx) = []
a.vm(idx) = []
a.vf(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)
