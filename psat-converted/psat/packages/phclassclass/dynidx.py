# Module: psat.packages.phclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE

if not a.n, return, end

for i in range(1, a.n+1):
  a.alpha(i) = DAE.n + 1
  a.Pm(i) = DAE.n + 2
  DAE.n = DAE.n + 2