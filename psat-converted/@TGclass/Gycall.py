# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

# Jacobian matrix Gy
global DAE

if not p.n, return, end

DAE.Gy = DAE.Gy - sparse(p.wref,p.wref,1,DAE.m,DAE.m)
