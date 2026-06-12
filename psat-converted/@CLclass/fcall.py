# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(p):

global DAE

if not p.n, return, end

Vs = DAE.x(p.Vs)
Qgr = p.con(:,7)

DAE.f(p.Vs) = (Qgr.*DAE.y(p.cac)-DAE.y(p.q)).*p.dVsdQ.*p.u

# anti-windup limits
fm_windup(p.Vs,p.con(:,8),p.con(:,9),'f')
