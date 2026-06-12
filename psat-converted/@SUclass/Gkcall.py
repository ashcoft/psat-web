# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\Gkcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gkcall(p):

global DAE

if not p.n, return, end

DAE.Gk = DAE.Gk - sparse(p.bus,1,p.u.*p.con(:,15).*p.con(:,3),DAE.m,1)
