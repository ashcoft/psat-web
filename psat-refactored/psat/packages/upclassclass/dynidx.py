# Module: psat.packages.upclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.vp = np.zeros((a.n,1))
a.vq = np.zeros((a.n,1))
a.iq = np.zeros((a.n,1))
a.vp0 = np.zeros((a.n,1))
a.vq0 = np.zeros((a.n,1))
a.vref = np.zeros((a.n,1))

for i in range(1, a.n+1):
  a.vp(i) = DAE.n + 1
  a.vq(i) = DAE.n + 2
  a.iq(i) = DAE.n + 3
  DAE.n = DAE.n + 3
  a.vp0(i) = DAE.m + 1
  a.vq0(i) = DAE.m + 2
  a.vref(i) = DAE.m + 3
  DAE.m = DAE.m + 3

a.gamma = np.zeros((a.n,1))