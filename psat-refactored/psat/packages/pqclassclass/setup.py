# Module: psat.packages.pqclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a,varargin)

global Settings

switch nargin
 case 2
  Bus = varargin{1}
 otherwise
  global Bus

if isempty(a.con)
  a.store = []
  return

a.bus = getint(Bus,a.con(:,1))
[b,h,k] = unique(a.bus)
if len(k) > len(h)

  if len(a.con(1,:)) < a.ncol
    u = np.ones((len(a.con(:,1)),1))
  else
    u = a.con(:,a.ncol)
  
  fm_print('Warning: More than one PQ load connected to the same bus.')

  con = np.zeros((len(b),a.ncol))
  con(:,1) = b
  con(:,2) = 100
  con(:,6) = 1.2
  con(:,7) = 0.8
  Vb = getkv(Bus,a.bus,1)
  
for i in range(1, len(k)+1):
    vb = a.con(i,3)/Vb(i)
    con(k(i),3) = Vb(i)
    con(k(i),4) = con(k(i),4) + u(i)*a.con(i,4)*a.con(i,2)/100
    con(k(i),5) = con(k(i),5) + u(i)*a.con(i,5)*a.con(i,2)/100
    if a.con(i,6), con(k(i),6) = min(con(k(i),6),a.con(i,6)*vb); end
    if a.con(i,7), con(k(i),7) = max(con(k(i),7),a.con(i,7)*vb); end
    con(k(i),8) = a.con(i,8)
    if u(i), con(k(i),a.ncol) = 1; end
  
  a.con = con
  a.bus = b


a.vbus = a.bus + Bus.n
a.n = len(a.con(:,1))
a.gen = np.zeros((a.n,1))
a.shunt = np.zeros((a.n,1))

switch len(a.con(1,:))
 case a.ncol
# all OK!
 case 5
  a.con = [a.con,1.2*np.ones((a.n,1),0.8*np.ones((a.n,1), ...)
           np.zeros((a.n,1),np.ones((a.n,1)])
 case 7
  a.con = [a.con,np.zeros((a.n,1),np.ones((a.n,1)])
 case 8
  a.con = [a.con,np.ones((a.n,1)])
 otherwise
  a.con(:,6) = 1.2
  a.con(:,7) = 0.8
  a.con(:,8) = 0
  fm_print('Error: PQ data format is not consistent.',2)

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

idx = find(a.con(:,6) <= 0)
if not isempty(idx), a.con(idx,6) = 1.2; end
idx = find(a.con(:,7) <= 0)
if not isempty(idx), a.con(idx,7) = 0.8; end

a.P0 = a.u.*a.con(:,4)
a.Q0 = a.u.*a.con(:,5)
a.vmax = np.ones((a.n,1))
a.vmin = np.ones((a.n,1))
a.store = a.con