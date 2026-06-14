# Module: psat.packages.tgclassclass.glambda
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda, kg):

global DAE

if not p.n, return, end

DAE.g = DAE.g - sparse(p.pm,1,(kg+lambda-1)*p.u.*pmech(p),DAE.m,1)