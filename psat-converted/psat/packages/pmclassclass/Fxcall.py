# Module: psat.packages.pmclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(a):

global DAE

if not a.n, return, end

DAE.Fx = DAE.Fx - sparse(a.vm,a.vm,a.dat(:,1),DAE.n,DAE.n)
DAE.Fx = DAE.Fx - sparse(a.thetam,a.thetam,a.dat(:,2),DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(a.vm,a.vbus,a.u.*a.dat(:,1),DAE.n,DAE.m)
DAE.Fy = DAE.Fy + sparse(a.thetam,a.bus,a.u.*a.dat(:,2),DAE.n,DAE.m)