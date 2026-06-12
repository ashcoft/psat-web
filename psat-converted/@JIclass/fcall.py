# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@JIclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

x = DAE.x(a.x)
V1 = DAE.y(a.vbus)
iTf = a.u./a.con(:,5)

DAE.f(a.x) = -(V1.*iTf+x).*iTf
