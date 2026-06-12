# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(a):

if not a.n, return, end

global DAE

DAE.Gl(a.pm) = -a.pm0.*a.u
DAE.Gk(a.pm) = -a.pm0.*a.u
