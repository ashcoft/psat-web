# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@JIclass\Fxcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(a):

global DAE

if not a.n, return, end

iTf = a.u./a.con(:,5)
Kv = a.u.*a.con(:,12)

DAE.Fx = DAE.Fx + sparse(a.x,a.x,-iTf,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(a.x,a.vbus,-iTf.*iTf,DAE.n,DAE.m)
DAE.Gx = DAE.Gx + sparse(a.vbus,a.x,Kv,DAE.m,DAE.n)
