# Module: psat.packages.bfclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(a):

global DAE

if not a.n, return, end

iTf = 1./a.con(:,2)
iTw = 1./a.con(:,3)
k = a.u.*a.dat(:,2)

DAE.Fx = DAE.Fx + sparse(a.x,a.x,-iTf,DAE.n,DAE.n)
DAE.Fx = DAE.Fx + sparse(a.w,a.x,-a.u.*iTw,DAE.n,DAE.n)
DAE.Fx = DAE.Fx + sparse(a.w,a.w,-iTw,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(a.x,a.bus,k.*iTf,DAE.n,DAE.m)
DAE.Fy = DAE.Fy + sparse(a.w,a.bus,k.*iTw,DAE.n,DAE.m)