# Module: psat.packages.flclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(a):

global DAE Settings

if not a.n, return, end

DAE.Fx = DAE.Fx - sparse(a.x,a.x,not a.u,DAE.n,DAE.n)
DAE.Fy = DAE.Fy - sparse(a.x,a.dw,a.u./a.con(:,8),DAE.n,DAE.m)
DAE.Gx = DAE.Gx + sparse(a.dw,a.x,a.u,DAE.m,DAE.n)