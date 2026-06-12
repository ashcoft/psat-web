# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DMclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(p):

global DAE

if not p.n, return, end

DAE.Gl = DAE.Gl + sparse(p.bus,1,p.u.*p.con(:,3),DAE.m,1)
DAE.Gl = DAE.Gl + sparse(p.vbus,1,p.u.*p.con(:,4),DAE.m,1)

