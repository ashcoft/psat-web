# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@THclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

T = DAE.x(a.T)
x = DAE.x(a.x)
G = DAE.y(a.G)
V = DAE.y(a.vbus)
Ki = a.con(:,4)
Ti = a.con(:,5)
T1 = a.con(:,6)
Ta = a.con(:,7)
Tref = a.con(:,8)
K1 = a.con(:,10)

DAE.f(a.T) = a.u.*(Ta - T + K1.*G.*V.^2)./T1
DAE.f(a.x) = a.u.*Ki.*(Tref-T)./Ti

# anti-windup limits
fm_windup(a.x,a.con(:,9),0,'f')
