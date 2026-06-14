# Module: psat.packages.stclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE

if not a.n, return, end

a.ist = DAE.n + [1:a.n]';
DAE.n = DAE.n + a.n
a.vref = DAE.m + [1:a.n]';
DAE.m = DAE.m + a.n