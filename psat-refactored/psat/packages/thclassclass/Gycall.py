# Module: psat.packages.thclassclass.Gycall
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
  + sparse(a.bus,a.vbus,2*DAE.y(a.G).*V,DAE.m,DAE.m) ...
  - sparse(a.G,a.G,a.u,DAE.m,DAE.m) ...
  + sparse(a.bus,a.G,V.*V,DAE.m,DAE.m)