# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BFclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

x = DAE.x(a.x)
w = DAE.x(a.w)
theta = DAE.y(a.bus)
iTf = a.u./a.con(:,2)
iTw = a.u./a.con(:,3)
theta0 = a.dat(:,1)
k = a.dat(:,2)

DAE.f(a.x) = (k.*(theta-theta0)-x).*iTf
DAE.f(a.w) = (-x+k.*(theta-theta0)+1-w).*iTw
