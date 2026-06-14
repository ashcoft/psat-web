# Module: psat.packages.pvclassclass.glambda
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda, kg):

global DAE

if not p.n, return, end

DAE.g(p.bus) = DAE.g(p.bus) - p.u.*(lambda+kg*p.con(:,10)).*p.con(:,4)