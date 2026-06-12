# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@UPclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = add(a,data)

global Line Bus

a.n = a.n + len(data(1,:))
a.con = [a.con; data]
a.line = [a.line; a.con(:,1)]
a.bus1 = [a.bus1; Line.fr(a.line)]
a.bus2 = [a.bus2; Line.to(a.line)]
a.v1 = a.bus1 + Bus.n
a.v2 = a.bus2 + Bus.n
