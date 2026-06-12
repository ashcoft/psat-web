# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TPclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

m = DAE.x(a.m)
V = DAE.y(a.vbus)
a1 = a.con(:,11)
a2 = a.con(:,12)

DAE.Gy = DAE.Gy + sparse(a.bus,a.vbus, ...
          a.u.*a.con(:,9).*a1.*(V.^(a1-1))./(m.^a1),DAE.m,DAE.m)

DAE.Gy = DAE.Gy + sparse(a.vbus,a.vbus, ...
          a.u.*a.con(:,10).*a2.*(V.^(a2-1))./(m.^a2),DAE.m,DAE.m)

