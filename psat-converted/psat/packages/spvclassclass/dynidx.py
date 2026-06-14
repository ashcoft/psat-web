# Module: psat.packages.spvclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.btx1 = np.zeros((a.n,1))
a.id = np.zeros((a.n,1))
a.iq = np.zeros((a.n,1))
a.vref = np.zeros((a.n,1))

for i in range(1, a.n+1):
  a.btx1(i) = DAE.n + 1
  a.id(i) = DAE.n + 2
  a.iq(i) = DAE.n + 3
  DAE.n = DAE.n + 3
  a.vref(i) = DAE.m + 1
  DAE.m = DAE.m + 1