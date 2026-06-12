# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CCclass\Fxcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(p):

global DAE

if not p.n, return, end

q1 = DAE.x(p.q1)
KI = p.con(:,6)

u = p.u & q1 < p.con(:,8) & q1 > p.con(:,9)

DAE.Gx = DAE.Gx + sparse(p.q,p.q1,u,DAE.m,DAE.n)
DAE.Fx = DAE.Fx - sparse(p.q1,p.q1,not u,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(p.q1,p.vbus,-KI.*u,DAE.n,DAE.m)
