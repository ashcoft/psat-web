# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@MNclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(a):

if not a.n, return, end

global DAE

V = DAE.y(a.vbus)

DAE.Gl = DAE.Gl + ...
         sparse(a.bus, 1, a.u.*a.con(:,4).*V.^a.con(:,6),DAE.m,1) + ...
         sparse(a.vbus,1, a.u.*a.con(:,5).*V.^a.con(:,7),DAE.m,1)
