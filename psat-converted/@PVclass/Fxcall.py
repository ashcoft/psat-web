# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\Fxcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(p):

global DAE

if not p.n, return, end

idx = p.vbus(find(p.u))

if isempty(idx),return, end

DAE.Fy(:,idx) = 0
DAE.Gx(idx,:) = 0
