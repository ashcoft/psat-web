# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def gcall(a):

global DAE

if not a.n, return, end

delta = np.zeros((a.n,1))
omega = np.ones((a.n,1))

for i in range(1, a.n+1):
  idx = a.syn{i}
  delta(i) = sum(a.M(idx).*DAE.x(a.dgen(idx)))/a.Mtot(i)
  omega(i) = sum(a.M(idx).*DAE.x(a.wgen(idx)))/a.Mtot(i)

DAE.g = DAE.g ...
    + sparse(a.delta,1,delta-DAE.y(a.delta),DAE.m,1) ...
    + sparse(a.omega,1,omega-DAE.y(a.omega),DAE.m,1)

