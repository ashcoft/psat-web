# Module: psat.packages.wtfrclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global DAE

if not p.n, return, end

DAE.Gy = DAE.Gy - sparse(p.pf1, p.pf1, 1, DAE.m, DAE.m)
DAE.Gy = DAE.Gy - sparse(p.pwa, p.pwa, 1, DAE.m, DAE.m)
#DAE.Gy = DAE.Gy - sparse(p.pout, p.pout, 1, DAE.m, DAE.m);