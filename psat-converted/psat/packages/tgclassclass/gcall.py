# Module: psat.packages.tgclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

# computes algebraic equations g
global DAE

if not p.n, return, end

DAE.g = DAE.g ...
    + sparse(p.pm,1,p.u.*pmech(p),DAE.m,1) ...
    + sparse(p.wref,1,p.u.*p.con(:,3)-DAE.y(p.wref),DAE.m,1)