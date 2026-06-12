# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SSclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.vcs = np.zeros((a.n,1))
a.vpi = np.zeros((a.n,1))
a.v0 = np.zeros((a.n,1))
a.pref = np.zeros((a.n,1))

for i in range(1, a.n+1):
  if a.con(i,2) == 3
    a.vcs(i,1) = DAE.n + 1
    a.vpi(i,1) = DAE.n + 2
    DAE.n = DAE.n + 2
  else
    a.vcs(i,1) = DAE.n + 1
    DAE.n = DAE.n + 1
  a.v0(i) = DAE.m + 1
  a.pref(i) = DAE.m + 2
  DAE.m = DAE.m + 2

