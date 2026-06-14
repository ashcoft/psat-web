# Module: psat.solvers.zbuildpi
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

# This program forms the complex bus impedance matrix by the method
# of building algorithm.  Bus zero is taken as reference.
# This program is compatible with power flow data.
#  Copyright (C) 1998  by H. Saadat.

function [Zbus, linedata] = zbuildpi(linedata, gendata, yload)

# gendata generator data syn.con
ng = len(gendata(:,1))
nlg = gendata(:,1)
nrg = np.zeros((size(gendata(:,1))))
zg = gendata(:,7) + j*gendata(:,6)

nl = linedata(:,1)
nr = linedata(:,2)

R = linedata(:,8)
X = linedata(:,9)
ZB = R + j*X

nbr = len(linedata(:,1))
nbus = max(max(nl), max(nr))
nc = len(linedata(1,:))

BC = 0.5*linedata(:,10)
yc = np.zeros((nbus,1))
nlc = np.zeros((nbus,1))
nrc = np.zeros((nbus,1))

for n in range(1, nbus+1):
  yc(n) = 0
  nlc(n) = 0
  nrc(n) = n
for k in range(1, nbr+1):
    if nl(k) == n  or  nr(k) == n
      yc(n) = yc(n) + j*BC(k)

if exist('yload') == 1
  yload = yload.';
  yc = yc + yload

m = 0
havecc = 0; #  have cc ? 

for n in range(1, nbus+1):
  if abs(yc(n)) !=0
    m = m + 1
    nlcc(m) = nlc(n)
    nrcc(m) = nrc(n)
    zc(m) = 1/yc(n)
    havecc = 1

if havecc == 1 
  nlcc = nlcc'; 
  nrcc = nrcc'; 
  zc = zc.';
  nl = [nlg; nlcc; nl]
  nr = [nrg; nrcc; nr]
  ZB = [zg; zc; ZB]
else
  nl = [nlg; nl]
  nr = [nrg; nr]
  ZB = [zg; ZB]

# standard line data consist of line generator capacitor of line model and load
linedata = [nl nr real(ZB) imag(ZB)]
nbr = len(nl)
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
      tree = tree+1; # %new
    else 
      Zbus(n,n) = Zbus(n,n)*ZB(I)/(Zbus(n,n) + ZB(I))
    ntree(I) = 2

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
            if abs(Zbus(k,k)) != 0
for m in range(1, nbus+1):
                if m != n
                  Zbus(m,n) = Zbus(m,k)
                  Zbus(n,m) = Zbus(m,k)
              Zbus(n,n) = Zbus(k,k) + ZB(I)
              tree=tree+1; # %new
              nadd = 2
              ntree(I) = 2
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

print('end of zbus build')