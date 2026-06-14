# Module: psat.packages.svclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

global DAE

if not a.n, return, end

V = DAE.y(a.vbus)
B = a.u.*bsvc(a)

DAE.g = DAE.g ...
        - sparse(a.vbus,1,DAE.y(a.q),DAE.m,1) ...
        + sparse(a.q,1,B.*V.*V-DAE.y(a.q),DAE.m,1) ...
        + sparse(a.vref,1,a.con(:,8)-DAE.y(a.vref),DAE.m,1)