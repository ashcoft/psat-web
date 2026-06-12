# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@THclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE

if not a.n, return, end

a.T = DAE.n + [1:2:2*a.n]';
a.x = DAE.n + [2:2:2*a.n]';
DAE.n = DAE.n + 2*a.n

a.G = DAE.m + [1:a.n]';
DAE.m = DAE.m + a.n