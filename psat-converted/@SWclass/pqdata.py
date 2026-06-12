# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\pqdata.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function data = pqdata(a,idx,qlim,sp,lambda,one)

if not a.n, return, end

idx = idx(1)
data = [a.con(idx,[1 2 3 10 6 8 9]),0,1]
data(1,4) = -a.pg(idx)

switch qlim
 case 'qmax'
  data(1,5) = -a.con(idx,6)
  fm_print([sp,'SW gen. at bus #', fvar(a.bus(idx),4), ...
           ' reached Q_max at lambda = ',fvar(lambda-one,9)])
 case 'qmin'
  data(1,5) = -a.con(idx,7)
  fm_print([sp,'SW gen. at bus #', fvar(a.bus(Qmin_idx(1)),4), ...
           ' reached Q_min at lambda = ',fvar(lambda-one,9)])
 case 'qmaxl'
  data(1,5) = -a.con(idx,6)
 case 'qminl'
  data(1,5) = -a.con(idx,7)

