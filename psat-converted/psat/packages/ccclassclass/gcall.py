# Module: psat.packages.ccclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

global DAE

if not p.n, return, end

q1 = DAE.x(p.q1)
V1 = DAE.y(p.vbus)
Vpref = p.con(:,5)
KI = p.con(:,6)
KP = p.u.*p.con(:,7)

DAE.g = DAE.g + sparse(p.q,1,q1+KP.*(Vpref-V1)-DAE.y(p.q),DAE.m,1)