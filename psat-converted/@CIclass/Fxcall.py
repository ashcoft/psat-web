# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\Fxcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def Fxcall(a):

global DAE Settings Syn

if not a.n, return, end

for i in range(1, a.n+1):
  idx = a.syn{i}
  n = len(idx)
  odx = a.omega(i)*np.ones((n,1))
  DAE.Fy = DAE.Fy - sparse(a.dgen(idx),odx,2*np.pi*Settings.freq*Syn.u(idx),DAE.n,DAE.m)
  DAE.Gx = DAE.Gx + sparse(a.delta(i),a.dgen(idx),a.M(idx)/a.Mtot(i),DAE.m,DAE.n)
  DAE.Gx = DAE.Gx + sparse(a.omega(i),a.wgen(idx),a.M(idx)/a.Mtot(i),DAE.m,DAE.n)
