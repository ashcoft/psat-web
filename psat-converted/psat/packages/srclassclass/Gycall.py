# Module: psat.packages.srclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

id = a.u.*DAE.x(a.Id)
iq = a.u.*DAE.x(a.Iq)
V = DAE.y(a.vbus)
theta = DAE.y(a.bus)
delta = DAE.x(a.delta)
cdt = cos(delta-theta)
sdt = sin(delta-theta)

DAE.Gy = DAE.Gy + sparse(a.bus,a.bus,V.*cdt.*id-V.*sdt.*iq,DAE.m,DAE.m)
DAE.Gy = DAE.Gy - sparse(a.bus,a.vbus,sdt.*id+cdt.*iq,DAE.m,DAE.m)
DAE.Gy = DAE.Gy - sparse(a.vbus,a.bus,V.*sdt.*id+V.*cdt.*iq,DAE.m,DAE.m)
DAE.Gy = DAE.Gy + sparse(a.vbus,a.vbus,sdt.*iq-cdt.*id,DAE.m,DAE.m)