# Module: psat.packages.wtfrclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE Dfig Busfreq

if not a.n, return, end

a.Dfm = np.zeros((a.n,1))
a.x = np.zeros((a.n,1))
a.csi = np.zeros((a.n,1))
a.pfw = np.zeros((a.n,1))
a.pf1 = np.zeros((a.n, 1))
a.pwa = np.zeros((a.n, 1))

for i in range(1, a.n+1):
  a.Dfm(i) = DAE.n + 1
  a.x(i) = DAE.n + 2
  a.csi(i) = DAE.n + 3
  a.pfw(i) = DAE.n + 4
  DAE.n = DAE.n + 4
  a.pf1(i) = DAE.m + 1
  a.pwa(i) = DAE.m + 2
  DAE.m = DAE.m + 2

a.pout = Dfig.pwa(a.gen)
a.we = Dfig.omega_m(a.gen)
a.Df = Busfreq.w(a.freq)