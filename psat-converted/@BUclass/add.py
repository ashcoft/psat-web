# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BUclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [a,newbus] = add(a,data,name,idx,str)

global DAE

if isempty(data), return, end

[nrow,ncol] = size(data)
busmax = len(a.int)
nb = [1:nrow]';
data(:,1) = busmax + nb
newbus = data(:,1)
a.int = [a.int; a.n + nb]

DAE.y(2*a.n + nrow + nb) = data(:,3)
DAE.y(a.n + nb) = data(:,4)

a.n = a.n + nrow
DAE.m = DAE.m + 2*nrow
a.con = [a.con; data]
a.a = [1:a.n]';
a.v = a.a + a.n

# update algebraic variables
DAE.y = np.zeros((DAE.m,1))
DAE.g = np.zeros((DAE.m,1))
DAE.Gy = sparse(DAE.m,DAE.m)
DAE.y(a.a) = a.con(:,4)
DAE.y(a.v) = a.con(:,3)

if not isempty(a.names)
  if isempty(name)
for i in range(1, nrow+1):
      a.names{end+1,1} = [a.names{a.int(idx(i))},str]
  else
for i in range(1, nrow+1):
      a.names{end+1,1} = name{i}

a.Pl = [a.Pl; np.zeros((nrow,1)])
a.Ql = [a.Ql; np.zeros((nrow,1)])
a.Pg = [a.Pg; np.zeros((nrow,1)])
a.Qg = [a.Qg; np.zeros((nrow,1)])
