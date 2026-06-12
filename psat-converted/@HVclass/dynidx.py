# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@HVclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE

if not a.n, return, end

a.Idc = np.zeros((a.n,1))
a.xr = np.zeros((a.n,1))
a.xi = np.zeros((a.n,1))

a.cosa = np.zeros((a.n,1))
a.cosg = np.zeros((a.n,1))
a.phir = np.zeros((a.n,1))
a.phii = np.zeros((a.n,1))
a.Vrdc = np.zeros((a.n,1))
a.Vidc = np.zeros((a.n,1))
a.yr = np.zeros((a.n,1))
a.yi = np.zeros((a.n,1))

for i in range(1, a.n+1):

  a.Idc(i) = DAE.n + 1
  a.xr(i) = DAE.n + 2
  a.xi(i) = DAE.n + 3
  
  DAE.n = DAE.n + 3

  a.cosa(i) = DAE.m + 1
  a.cosg(i) = DAE.m + 2
  a.phir(i) = DAE.m + 3
  a.phii(i) = DAE.m + 4
  a.Vrdc(i) = DAE.m + 5
  a.Vidc(i) = DAE.m + 6
  a.yr(i) = DAE.m + 7
  a.yi(i) = DAE.m + 8
  
  DAE.m = DAE.m + 8
  

# extend the vector of algebraic variables 
DAE.y = [DAE.y; np.zeros((8*a.n,1)])
