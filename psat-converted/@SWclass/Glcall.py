# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\Glcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(p):

global DAE

if not p.n, return, end

jdx = find(p.u)
idx = p.bus(jdx)

if isempty(idx),return, end

DAE.Gl(idx) = DAE.Gl(idx) - p.pg(jdx)
