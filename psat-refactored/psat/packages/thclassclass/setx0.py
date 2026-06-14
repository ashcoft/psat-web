# Module: psat.packages.thclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setx0(a)

global DAE PQ

if not a.n, return, end

V = DAE.y(a.vbus)
T1 = a.con(:,6)
Ta = a.con(:,7)
Tref = a.con(:,8)
K1 = a.con(:,10)
KL = a.con(:,11)

Pl = np.zeros((a.n,1))

# get powers and update PQ loads
for i in range(1, a.n+1):
  idx = findbus(PQ,a.bus(i))
  if isempty(idx)
    warn(a,idx,' No PQ load found.')
  else
    Pl(i) = a.con(i,2)*PQ.P0(idx)/100
    PQ = pqsub(PQ,idx,a.u(i)*Pl(i),0)
    PQ = remove(PQ,idx,'zero')

G = Pl./V./V

DAE.y(a.G) = a.u.*G
DAE.x(a.x) = a.u.*G
DAE.x(a.T) = a.u.*Tref
a.con(:,10) = (Tref-Ta)./Pl

idx = find(T1 == 0)
if idx
  a.con(idx,8) = 1200
  warn(a,idx,' Found T1 = 0. Default value T1 = 1200 s will be used.')

idx = find(KL < 1); #  & KL != 0
if idx
  a.con(idx,11) = 2
  warn(a,idx,' Found KL < 1. Default value KL = 2 will be used.')

#idx = find(KL == 0);
#if ~isempty(idx), Gmax = a.con(idx,9); end

# fix G_max
a.con(:,9) = a.con(:,11).*G
#if ~isempty(idx), a.con(idx,9) = Gmax; end

fm_print('Initialization of Thermostatically Controlled Loads completed.')