# Module: psat.packages.csclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.omega_t = np.zeros((a.n,1))
a.omega_m = np.zeros((a.n,1))
a.gamma = np.zeros((a.n,1))
a.e1r = np.zeros((a.n,1))
a.e1m = np.zeros((a.n,1))
for i in range(1, a.n+1):
  a.omega_t(i) = DAE.n + 1
  a.omega_m(i) = DAE.n + 2
  a.gamma(i) = DAE.n + 3
  a.e1r(i) = DAE.n + 4
  a.e1m(i) = DAE.n + 5
  DAE.n = DAE.n + 5