# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\glambda.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(a, lambda, kg):

if not a.n, return, end

global DAE

DAE.g = DAE.g + sparse(a.pm,1,(1-lambda-kg)*a.pm0.*a.u,DAE.m,1)

