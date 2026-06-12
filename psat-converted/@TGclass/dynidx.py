# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)
# assigns indexes to the state variables
global DAE Syn

if not a.n, return, end

a.ty1 = find(a.con(:,2) == 1)
a.ty2 = find(a.con(:,2) == 2)
a.ty3 = find(a.con(:,2) == 3)
a.ty4 = find(a.con(:,2) == 4)
a.ty5 = find(a.con(:,2) == 5)
a.ty6 = find(a.con(:,2) == 6)
a.tg1 = np.zeros((a.n,1))
a.tg2 = np.zeros((a.n,1))
a.tg3 = np.zeros((a.n,1))
a.tg4 = np.zeros((a.n,1))
a.tg5 = np.zeros((a.n,1))
a.tg  = np.zeros((a.n,1))

for i in range(1, a.n+1):
  switch a.con(i,2)
   case 1
    a.tg1(i) = DAE.n + 1
    a.tg2(i) = DAE.n + 2
    a.tg3(i) = DAE.n + 3
    DAE.n = DAE.n + 3
   case 2
    a.tg(i) = DAE.n + 1
    DAE.n = DAE.n + 1
   case 3
    a.tg1(i) = DAE.n + 1
    a.tg2(i) = DAE.n + 2
    a.tg3(i) = DAE.n + 3
    a.tg4(i) = DAE.n + 4
    DAE.n = DAE.n + 4
   case 4
    a.tg1(i) = DAE.n + 1
    a.tg2(i) = DAE.n + 2
    a.tg3(i) = DAE.n + 3
    a.tg4(i) = DAE.n + 4
    a.tg5(i) = DAE.n + 5
    DAE.n = DAE.n + 5
   case 5
    a.tg1(i) = DAE.n + 1
    a.tg2(i) = DAE.n + 2
    a.tg3(i) = DAE.n + 3
    a.tg4(i) = DAE.n + 4
    DAE.n = DAE.n + 4
   case 6
    a.tg1(i) = DAE.n + 1
    a.tg2(i) = DAE.n + 2
    a.tg3(i) = DAE.n + 3
    a.tg4(i) = DAE.n + 4
    a.tg5(i) = DAE.n + 5
    DAE.n = DAE.n + 5

a.wref = DAE.m + [1:a.n]';
DAE.m = DAE.m + a.n

a.pm = Syn.pm(a.syn)
