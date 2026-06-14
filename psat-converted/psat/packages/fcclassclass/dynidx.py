# Module: psat.packages.fcclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE

if not a.n, return, end

m = 7
k = [0:m:m*(a.n-1)]';

a.Ik   = DAE.n + 1 + k
a.Vk   = DAE.n + 2 + k
a.pH2  = DAE.n + 3 + k
a.pH2O = DAE.n + 4 + k
a.pO2  = DAE.n + 5 + k
a.qH2  = DAE.n + 6 + k
a.m    = DAE.n + 7 + k

DAE.n = DAE.n + m*a.n