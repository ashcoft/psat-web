# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE Syn

if not a.n, return, end

a.vm  = np.zeros((a.n,1))
a.vr1 = np.zeros((a.n,1))
a.vr2 = np.zeros((a.n,1))
a.vr3 = np.zeros((a.n,1))
a.vf = np.zeros((a.n,1))
a.vfd = Syn.vf(a.syn)

a.vref0 = np.ones((a.n,1))
a.vref  = DAE.m + [1:a.n]';
DAE.m = DAE.m + a.n

for i in range(1, a.n+1):
  switch a.con(i,2)
   case 1
    a.vm(i)  = DAE.n + 1
    a.vr1(i) = DAE.n + 2
    a.vr2(i) = DAE.n + 3
    a.vf(i) = DAE.n + 4
    DAE.n = DAE.n + 4
   case 2
    a.vm(i)  = DAE.n + 1
    a.vr1(i) = DAE.n + 2
    a.vr2(i) = DAE.n + 3
    a.vf(i) = DAE.n + 4
    DAE.n = DAE.n + 4
   case 3
    a.vm(i)  = DAE.n + 1
    a.vr3(i) = DAE.n + 2
    a.vf(i) = DAE.n + 3
    DAE.n = DAE.n + 3
