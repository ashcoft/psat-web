# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PHclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(p):

global DAE Settings

if not p.n, return, end

alpha = DAE.x(p.alpha)
Pm = DAE.x(p.Pm)

Vf = p.u.*DAE.y(p.v1).*exp(i*DAE.y(p.bus1))
Vt = p.u.*DAE.y(p.v2).*exp(i*DAE.y(p.bus2))
y = admittance(p)
m = p.con(:,15).*exp(i*alpha)
errP = real(Vf.*conj((Vf./m-Vt).*y./conj(m)))-Pm

Tm = p.con(:,7)
Kp = p.con(:,8)
Ki = p.con(:,9)
Pref = p.u.*p.con(:,10)

DAE.f(p.alpha) = Kp.*errP./Tm+Ki.*(Pm-Pref)
DAE.f(p.Pm) = errP./Tm

# non-windup limits
fm_windup(p.alpha,p.con(:,13),p.con(:,14),'pf')
