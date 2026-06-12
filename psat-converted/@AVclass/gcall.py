# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

global DAE

if not p.n, return, end

DAE.g = DAE.g + sparse(p.vfd,1,DAE.x(p.vf),DAE.m,1)
DAE.g = DAE.g + sparse(p.vref,1,p.u.*p.vref0-DAE.y(p.vref),DAE.m,1)
