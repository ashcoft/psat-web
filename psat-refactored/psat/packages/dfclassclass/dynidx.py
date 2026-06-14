# Module: psat.packages.dfclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.theta_p = np.zeros((a.n,1))
a.omega_m = np.zeros((a.n,1))
a.idr = np.zeros((a.n,1))
a.iqr = np.zeros((a.n,1))
a.vref = np.zeros((a.n,1))
a.pwa = np.zeros((a.n,1))
for i in range(1, a.n+1):
  a.omega_m(i) = DAE.n + 1
  a.theta_p(i) = DAE.n + 2
  a.idr(i) = DAE.n + 3
  a.iqr(i) = DAE.n + 4
  DAE.n = DAE.n + 4
  a.pwa(i) = DAE.m + 1
  a.vref(i) = DAE.m + 2
  DAE.m = DAE.m + 2