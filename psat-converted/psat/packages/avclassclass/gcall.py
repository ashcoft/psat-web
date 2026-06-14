# Module: psat.packages.avclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

global DAE

if not p.n, return, end

DAE.g = DAE.g + sparse(p.vfd,1,DAE.x(p.vf),DAE.m,1)
DAE.g = DAE.g + sparse(p.vref,1,p.u.*p.vref0-DAE.y(p.vref),DAE.m,1)