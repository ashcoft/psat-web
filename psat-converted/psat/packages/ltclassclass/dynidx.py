# Module: psat.packages.ltclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE

if not a.n, return, end

a.mc = DAE.n + [1:a.n]';
DAE.n = DAE.n + a.n

a.md = DAE.m + [1:a.n]';
DAE.m = DAE.m + a.n