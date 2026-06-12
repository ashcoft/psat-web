# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\Glreac.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glreac(p):

global DAE

if not p.n, return, end

idx = p.vbus(find(p.u))

if isempty(idx),return, end

DAE.Gl(idx) = 0
