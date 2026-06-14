# Module: psat.packages.oxclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

global DAE

if not a.n, return, end

dipqv = ifield(a,2)

DAE.Gy = DAE.Gy ...
         - sparse(a.If,a.If,1,DAE.m,DAE.m) ...
         + sparse(a.If,a.p,dipqv(:,1),DAE.m,DAE.m) ...
         + sparse(a.If,a.q,dipqv(:,2),DAE.m,DAE.m) ...
         + sparse(a.If,a.vbus,dipqv(:,3),DAE.m,DAE.m)