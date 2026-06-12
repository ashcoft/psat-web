# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\diagy.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function YBB = diagy(a)

YBB = []

if not a.n, return, end

r = a.con(:,8)
x = a.con(:,9)
z = r + i*x
y = a.u./z
YBB = diag(y)
