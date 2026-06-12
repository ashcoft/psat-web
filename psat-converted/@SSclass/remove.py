# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SSclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.line(idx) = []
a.bus1(idx) = []
a.bus2(idx) = []
a.v1(idx) = []
a.v2(idx) = []
a.n = a.n - len(idx)
a.y(idx) = []
a.u(idx) = []
a.pref(idx) = []
a.Pref(idx) = []
a.Cp(idx) = []
a.xcs(idx) = []
a.vcs(idx) = []
a.vpi(idx) = []
a.v0(idx) = []
a.V0(idx) = []
