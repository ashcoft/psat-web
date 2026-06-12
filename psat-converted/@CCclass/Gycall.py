# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CCclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global DAE

if not p.n, return, end

KP = p.u.*p.con(:,7)

DAE.Gy = DAE.Gy - sparse(p.q,p.q,1,DAE.m,DAE.m)
DAE.Gy = DAE.Gy - sparse(p.q,p.vbus,KP,DAE.m,DAE.m)
