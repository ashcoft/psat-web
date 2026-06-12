# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@HVclass\windup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def windup(a):

if not a.n, return, end

fm_windup(a.xr,a.dat(:,3),a.dat(:,4),'td')
fm_windup(a.xi,a.dat(:,5),a.dat(:,6),'td')
