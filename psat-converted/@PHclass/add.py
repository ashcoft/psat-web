# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PHclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = add(a,data)

global Bus

a.n = a.n + len(data(1,:))
a.con = [a.con; data]
[a.bus1,a.v1] = getbus(Bus,a.con(:,1))
[a.bus2,a.v2] = getbus(Bus,a.con(:,2))

