# Module: psat.packages.svclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

V = a.u.*DAE.y(a.vbus)

DAE.Gy = DAE.Gy ...
         - sparse(a.vbus,a.q,1,DAE.m,DAE.m) ...
         + sparse(a.q,a.vbus,2*a.Be.*V,DAE.m,DAE.m) ...
         - sparse(a.q,a.q,1,DAE.m,DAE.m) ...
         - sparse(a.vref,a.vref,1,DAE.m,DAE.m)