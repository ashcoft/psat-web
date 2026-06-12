# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WNclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(a):

global DAE

if not a.n, return, end

DAE.Gl = DAE.Gl + sparse(a.ws,1,wspeed(a),DAE.m,1)
