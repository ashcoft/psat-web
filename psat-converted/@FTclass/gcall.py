# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FTclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(p):

global DAE

if not p.n, return, end

V = DAE.y(p.vbus)
V2 = p.u.*V.*V

DAE.g = DAE.g + ...
        sparse(p.bus,1,p.dat(:,1).*V2,DAE.m,1) - ...
        sparse(p.vbus,1,p.dat(:,2).*V2,DAE.m,1)
