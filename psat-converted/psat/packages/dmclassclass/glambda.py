# Module: psat.packages.dmclassclass.glambda
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda):

global DAE

if not p.n, return, end

DAE.g = DAE.g + sparse(p.bus,1,lambda*p.u.*p.con(:,3),DAE.m,1) ...
        + sparse(p.vbus,1,lambda*p.u.*p.con(:,4),DAE.m,1)