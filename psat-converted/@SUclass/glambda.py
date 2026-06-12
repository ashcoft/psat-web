# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\glambda.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda, kg):

global DAE

if not p.n, return, end

DAE.g = DAE.g - sparse(p.bus,1,(lambda+kg*p.con(:,15)).*p.u.*p.con(:,3),DAE.m,1)
