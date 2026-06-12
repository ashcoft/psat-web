# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@JIclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

V1 = DAE.y(a.vbus)
Tf = a.con(:,5)
Plz = a.con(:,6)
Pli = a.con(:,7)
Qlz = a.con(:,9)
Qli = a.con(:,10)
Kv = a.con(:,12)
V1_0 = a.dat(:,1)

DAE.Gy = DAE.Gy + sparse(a.bus,a.vbus, ...
                           a.u.*(2.*Plz.*V1./V1_0.^2+Pli./V1_0),DAE.m,DAE.m)
DAE.Gy = DAE.Gy + sparse(a.vbus,a.vbus, ...
                           a.u.*(2.*Qlz.*V1./V1_0.^2+Qli./V1_0+Kv./Tf),DAE.m,DAE.m)
