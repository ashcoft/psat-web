# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@IMclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.slip = np.zeros((a.n,1))
a.e1r = np.zeros((a.n,1))
a.e1m = np.zeros((a.n,1))
a.e2r = np.zeros((a.n,1))
a.e2m = np.zeros((a.n,1))

for i in range(1, a.n+1):
  mot_ord = a.con(i,5)
  switch mot_ord
   case 1
    a.slip(i) = DAE.n + 1
    DAE.n = DAE.n+1
   case 3
    a.slip(i) = DAE.n + 1
    a.e1r(i) = DAE.n + 2
    a.e1m(i) = DAE.n + 3
    DAE.n = DAE.n+3
   case 5
    a.slip(i) = DAE.n + 1
    a.e1r(i) = DAE.n + 2
    a.e1m(i) = DAE.n + 3
    a.e2r(i) = DAE.n + 4
    a.e2m(i) = DAE.n + 5
    DAE.n = DAE.n+5
