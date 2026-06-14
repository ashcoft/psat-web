# Module: psat.packages.pvclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a,varargin)

if isempty(a.con)
  a.store = []
  return

global DAE Settings

switch nargin
 case 2
  Bus = varargin{1}
 otherwise
  global Bus

a.bus = getint(Bus,a.con(:,1))
[b,h,k] = unique(a.bus)

if len(k) > len(h)

  fm_print('Warning: More than one PV generator connected to the same bus.')

  if len(a.con(1,:)) < a.ncol
    u = np.ones((len(a.con(:,1)),1))
  else
    u = a.con(:,a.ncol)

  con = np.zeros((len(b),a.ncol))
  con(:,1) = b
  con(:,2) = 100
  con(:,8) = 1.2
  con(:,9) = 0.8

for i in range(1, len(k)+1):
    vb = a.con(i,3)/Bus.con(a.bus(i),2)
    con(k(i),3) = Bus.con(a.bus(i),2)
    con(k(i),4) = con(k(i),4) + u(i)*a.con(i,4)*a.con(i,2)/100
    con(k(i),5) = a.con(i,5)*vb
    con(k(i),6) = con(k(i),6) + u(i)*a.con(i,6)*a.con(i,2)/100
    con(k(i),7) = con(k(i),7) + u(i)*a.con(i,7)*a.con(i,2)/100
    if a.con(i,8), con(k(i),8) = min(con(k(i),8),a.con(i,8)*vb); end
    if a.con(i,9), con(k(i),9) = max(con(k(i),9),a.con(i,9)*vb); end
    con(k(i),10) = a.con(i,10)
    if u(i), con(k(i),a.ncol) = 1; end

  a.con = con
  a.bus = b


a.vbus = a.bus + Bus.n
a.n = len(a.con(:,1))
DAE.y(a.vbus) = a.con(:,5)

switch len(a.con(1,:))
 case a.ncol
# All OK!
 case 5
  a.con = [a.con, 999*np.ones((a.n,1), ...)
           -999*np.ones((a.n,1), 1.1*np.ones((a.n,1), ...)
           0.9*np.ones((a.n,1), np.ones((a.n,2)])
 case 9
  a.con = [a.con, np.ones((a.n,2)])
 case 10
  a.con = [a.con, np.ones((a.n,1)])

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

# fix reactive power limits
idx = find(a.con(:,6) == 0 & a.con(:,7) == 0)
if not isempty(idx)
  a.con(:,6) =  99*Settings.mva
  a.con(:,7) = -99*Settings.mva

a.qmax = np.ones((a.n,1))
a.qmin = np.ones((a.n,1))
a.pq = np.zeros((a.n,1))
a.qg = np.zeros((a.n,1))
a.store = a.con