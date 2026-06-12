# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SVclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.bcv = np.zeros((a.n,1))
a.alpha = np.zeros((a.n,1))
a.vm = np.zeros((a.n,1))
a.vref = np.zeros((a.n,1))
a.q = np.zeros((a.n,1))

type = a.con(:,5)

for i in range(1, a.n+1):
  if type(i) == 1
    a.bcv(i) = DAE.n + 1
    DAE.n = DAE.n + 1
  elseif type(i) == 2
    a.alpha(i) = DAE.n + 1
    a.vm(i) = DAE.n + 2
    DAE.n = DAE.n + 2
  a.vref(i) = DAE.m + 1
  a.q(i) = DAE.m + 2
  DAE.m = DAE.m + 2

a.bcv = a.bcv(find(a.bcv))
a.alpha = a.alpha(find(a.alpha))
a.vm = a.vm(find(a.vm))
a.Be = np.zeros((a.n,1))

