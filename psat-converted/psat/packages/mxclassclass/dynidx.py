# Module: psat.packages.mxclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.x = np.zeros((a.n,1))
a.y = np.zeros((a.n,1))
for i in range(1, a.n+1):
  a.x(i) = DAE.n + 1
  a.y(i) = DAE.n + 2
  DAE.n = DAE.n + 2