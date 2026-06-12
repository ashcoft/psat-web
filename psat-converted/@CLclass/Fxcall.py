# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\Fxcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(p):

global DAE

if not p.n, return, end

Vs = DAE.x(p.Vs)
u = p.u & Vs < p.con(:,8) & Vs > p.con(:,9)

DAE.Gx = DAE.Gx + sparse(p.vref,p.Vs,u,DAE.m,DAE.n)
DAE.Fx = DAE.Fx - sparse(p.Vs,p.Vs,not u,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(p.Vs,p.cac,u.*p.con(:,7).*p.dVsdQ,DAE.n,DAE.m) ...
         - sparse(p.Vs,p.q,u.*p.dVsdQ,DAE.n,DAE.m)
