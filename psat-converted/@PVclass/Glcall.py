# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(p):

global DAE

if not p.n, return, end

DAE.Gl(p.bus) = DAE.Gl(p.bus) - p.u.*p.con(:,4)
