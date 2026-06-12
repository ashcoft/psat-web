# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE Syn

if not a.n, return, end

a.delta = np.zeros((a.n,1))
a.omega = np.zeros((a.n,1))

for i in range(1, a.n+1):
  a.delta(i) = DAE.m + 1
  a.omega(i) = DAE.m + 2
  DAE.m = DAE.m + 2

a.dgen = Syn.delta(a.gen)
a.wgen = Syn.omega(a.gen)
