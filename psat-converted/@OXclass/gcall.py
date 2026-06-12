# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@OXclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

global DAE Exc

if not p.n, return, end

DAE.g = DAE.g - sparse(Exc.vref(p.exc),1,DAE.x(p.v),DAE.m,1)
DAE.g = DAE.g + sparse(p.If,1,ifield(p,1)-DAE.y(p.If),DAE.m,1)

