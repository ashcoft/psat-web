# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\setgamma.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setgamma(a)

z = a.con(:,12)
a.u = a.con(:,a.ncol)

a.con(find(z & a.u),11) = 1
