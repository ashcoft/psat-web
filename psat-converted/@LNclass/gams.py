# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\gams.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [n,data,Li,Lj,Gh,Bh,Ghc,Bhc] = gams(a,method)

global Bus GAMS Settings

n = int2str(a.n)
nl = [1:a.n]
nb = Bus.n

# Flows on transmission lines
tps = a.con(:,11).*exp(j*a.con(:,12)*np.pi/180)
r = a.con(:,8)
x = a.con(:,9)
chrg =  a.u.*a.con(:,10)/2
z = r + j*x
y = a.u./z
g = real(y)
b = imag(y)
m = tps.*conj(tps)
y1 = tps.*y./m
g1 = real(y1)
b1 = imag(y1)
g0 = g./m

if GAMS.flow == 1  or  GAMS.flow == 3
  b0 = chrg
else
  b0 = chrg-b./m

switch method
 case 1
  Li = []
  Lj = []
 case 2
  Li = sparse(nl,a.fr,b,a.n,nb)
  Lj = sparse(nl,a.to,b,a.n,nb)
 otherwise
  Li = sparse(nl,a.fr,1,a.n,nb)
  Lj = sparse(nl,a.to,1,a.n,nb)

if method != 1
  Gh = real(a.Y)
  Bh = imag(a.Y)
  Gh(1,1) = Gh(1,1) + 1e-8
  Bh(1,1) = Bh(1,1) + 1e-8
else
  Gh = []
  Bh = []

switch method
 case {4,6,7}
  if GAMS.line
    a.u(GAMS.line) = 0
    a = build_y(a)
    Ghc = real(a.Y)
    Bhc = imag(a.Y)
  else
    Ghc = Gh
    Bhc = Bh
 otherwise
  Ghc = []
  Bhc = []

if GAMS.flow
  Pijmax = getflowmax(a,GAMS.flow)
  Pjimax = Pijmax
else
  Pijmax = 999*Settings.mva*np.ones((a.n,1))
  Pjimax = 999*Settings.mva*np.ones((a.n,1))

data.val = [g1,b1,g0,b0,Pijmax,Pjimax]
data.labels = {cellstr(num2str([1:a.n]')), ...
	    {'g','b','g0','b0','Pijmax','Pjimax'}}
data.name = 'N'
