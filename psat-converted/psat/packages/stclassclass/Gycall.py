# Module: psat.packages.stclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

DAE.Gy = DAE.Gy ...
         - sparse(a.vbus,a.vbus,a.u.*DAE.x(a.ist),DAE.m,DAE.m) ...
         - sparse(a.vref,a.vref,1,DAE.m,DAE.m)
         
