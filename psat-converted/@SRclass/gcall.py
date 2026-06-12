# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SRclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

global DAE

if not a.n, return, end

id = DAE.x(a.Id)
iq = DAE.x(a.Iq)
V = a.u.*DAE.y(a.vbus)
theta = DAE.y(a.bus)
delta = DAE.x(a.delta)
cdt = cos(delta-theta)
sdt = sin(delta-theta)

DAE.g = DAE.g - sparse(a.bus,1,V.*sdt.*id+V.*cdt.*iq,DAE.m,1) ...
        - sparse(a.vbus,1,V.*cdt.*id-V.*sdt.*iq,DAE.m,1)
