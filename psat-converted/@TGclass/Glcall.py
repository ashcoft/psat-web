# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(p):

global DAE

if not p.n, return, end

DAE.Gl = DAE.Gl - sparse(p.pm,1,p.u.*pmech(p),DAE.m,1)
DAE.Gk = DAE.Gk - sparse(p.pm,1,p.u.*pmech(p),DAE.m,1)
