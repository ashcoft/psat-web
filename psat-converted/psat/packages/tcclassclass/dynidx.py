# Module: psat.packages.tcclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.x1 = np.zeros((a.n,1))
a.x2 = np.zeros((a.n,1))
a.x0 = np.zeros((a.n,1))
a.pref = np.zeros((a.n,1))

for i in range(1, a.n+1):
  a.x1(i) = DAE.n + 1
  if a.con(i,3) == 2
    a.x2(i) = DAE.n + 2
    DAE.n = DAE.n + 2
  else
    DAE.n = DAE.n + 1
  a.x0(i) = DAE.m + 1
  a.pref(i) = DAE.m + 2
  DAE.m = DAE.m + 2