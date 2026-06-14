# Module: psat.packages.tgclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

# Jacobian matrix Gy
global DAE

if not p.n, return, end

DAE.Gy = DAE.Gy - sparse(p.wref,p.wref,1,DAE.m,DAE.m)