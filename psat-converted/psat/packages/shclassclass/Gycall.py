# Module: psat.packages.shclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global DAE

if not p.n, return, end

V = 2*p.u.*DAE.y(p.vbus)

DAE.Gy  = DAE.Gy + ...
          sparse(p.bus, p.vbus,p.con(:,5).*V,DAE.m,DAE.m) - ...
          sparse(p.vbus,p.vbus,p.con(:,6).*V,DAE.m,DAE.m)
