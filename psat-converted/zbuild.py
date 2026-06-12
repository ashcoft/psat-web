# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/zbuild.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

# This program forms the complex bus impedance matrix by the method
# of building algorithm.  Bus zero is taken as reference.
#  Copyright (c) 1998  by H. Saadat
#

# Update By s.m. Shariatzadeh For Psat Data Format 

function [Zbus] = zbuild(linedata)

nl = linedata(:,1)
nr = linedata(:,2)

R = linedata(:,8)
X = linedata(:,9)

nbr = len(linedata(:,1))
nbus = max(max(nl), max(nr))

for k in range(1, nbr+1):
  if R(k) == inf  or  X(k) == inf
    R(k) = 99999999
    X(k) = 99999999

ZB = R + j*X
Zbus = np.zeros((nbus, nbus))
tree = 0;  # %%%new
         
# Adding a branch from a new bus to reference bus 0
for I in range(1, nbr+1):
  ntree(I) = 1
  if nl(I) == 0  or  nr(I) == 0
    if nl(I) == 0
      n = nr(I)
    elseif nr(I) == 0
      n = nl(I)
    if abs(Zbus(n, n)) == 0
      Zbus(n,n) = ZB(I)
      tree = tree + 1; # %new
    else 
      Zbus(n,n) = Zbus(n,n)*ZB(I)/(Zbus(n,n) + ZB(I))
    ntree(I) = 2

Zbus

# Adding a branch from new bus to an existing bus
while tree < nbus  # %% new

for n in range(1, nbus+1):
    nadd = 1
    if abs(Zbus(n,n)) == 0
for I in range(1, nbr+1):
        if nadd == 1
          if nl(I) == n  or  nr(I) == n
            if nl(I) == n
              k = nr(I)
            elseif nr(I) == n
              k = nl(I)
#if abs(Zbus(k,k)) != 0
for m in range(1, nbus+1):
              if m != n
                Zbus(m,n) = Zbus(m,k)
                Zbus(n,m) = Zbus(m,k)
            Zbus(n,n) = Zbus(k,k) + ZB(I); tree=tree+1; # %new
            nadd = 2;  ntree(I) = 2
#else, end

end  # %%%%%new

# Adding a link between two old buses
for n in range(1, nbus+1):
for I in range(1, nbr+1):
    if ntree(I) == 1
      if nl(I) == n  or  nr(I) == n
        if nl(I) == n
          k = nr(I)
        elseif nr(I) == n 
          k = nl(I)
        DM = Zbus(n,n) + Zbus(k,k) + ZB(I) - 2*Zbus(n,k)
for jj in range(1, nbus+1):
          AP = Zbus(jj,n) - Zbus(jj,k)
for kk in range(1, nbus+1):
            AT = Zbus(n,kk) - Zbus(k, kk)
            DELZ(jj,kk) = AP*AT/DM
        Zbus = Zbus - DELZ
        ntree(I) = 2
