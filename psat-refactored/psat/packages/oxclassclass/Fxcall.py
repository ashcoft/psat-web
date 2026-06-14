# Module: psat.packages.oxclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(p):

global DAE Exc

if not p.n, return, end

z = DAE.x(p.v) > 0 & DAE.x(p.v) < p.con(:,7) & p.u

DAE.Fx = DAE.Fx + sparse(p.v,p.v,-1e-6,DAE.n,DAE.n)
DAE.Fy = DAE.Fy + sparse(p.v,p.If,z./p.con(:,2),DAE.n,DAE.m)
DAE.Gx = DAE.Gx - sparse(p.vref,p.v,z,DAE.m,DAE.n)