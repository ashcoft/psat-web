# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

DAE.Gy = DAE.Gy ...
         - sparse(a.delta,a.delta,1,DAE.m,DAE.m) ...
         - sparse(a.omega,a.omega,1,DAE.m,DAE.m)
