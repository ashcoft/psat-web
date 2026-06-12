# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FTclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global DAE

if not p.n, return, end

V = 2*p.u.*DAE.y(p.vbus)

DAE.Gy  = DAE.Gy + ...
          sparse(p.bus, p.vbus,p.dat(:,1).*V,DAE.m,DAE.m) - ...
          sparse(p.vbus,p.vbus,p.dat(:,2).*V,DAE.m,DAE.m)

