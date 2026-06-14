# Module: psat.packages.wnclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(a):

global DAE

if not a.n, return, end

k = 1./a.con(:,4)
DAE.Fx = DAE.Fx - sparse(a.vw,a.vw,k,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(a.vw,a.ws,k,DAE.n,DAE.m)