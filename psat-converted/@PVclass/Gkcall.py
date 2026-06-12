# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\Gkcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gkcall(p):

global DAE

if not p.n, return, end

DAE.Gk(p.bus) = DAE.Gk(p.bus) - p.u.*p.con(:,10).*p.con(:,4)
