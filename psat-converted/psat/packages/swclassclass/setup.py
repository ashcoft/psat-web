# Module: psat.packages.swclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a,varargin)

global DAE Settings

switch nargin
 case 3
  Bus = varargin{1}
  PV = varargin{2}
 otherwise
  global Bus
  global PV

if isempty(a.con)
  a.store = []
  fm_print('Error: No slack bus found.',2)
  Settings.ok = 0
  return

a.n = len(a.con(:,1))
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))

b = unique(a.bus)
if a.n > len(b)
  fm_print(['Error: More than one slack generator ', ...
           'connected to the same bus.'],2)
  Settings.ok = 0
  return

switch len(a.con(1,:))
 case 5
  a.con = [a.con, 999*np.ones((a.n,1), -999*np.ones((a.n,1), ...)
           1.1*np.ones((a.n,1), 0.9*np.ones((a.n,1), ...)
           np.zeros((a.n,1), np.ones((a.n,3)])
 case 6
  a.con = [a.con, -999*np.ones((a.n,1), ...)
           1.1*np.ones((a.n,1), 0.9*np.ones((a.n,1), ...)
           np.zeros((a.n,1), np.ones((a.n,3)])
 case 7
  a.con = [a.con, 1.1*np.ones((a.n,1), 0.9*np.ones((a.n,1), ...)
           np.zeros((a.n,1), np.ones((a.n,3)])
 case 8
  a.con = [a.con, 0.9*np.ones((a.n,1), ...)
           np.zeros((a.n,1), np.ones((a.n,3)])
 case 9
  a.con = [a.con, np.zeros((a.n,1), np.ones((a.n,3)])
 case 10
  a.con = [a.con, np.ones((a.n,3)])
 case 11
  a.con = [a.con, np.ones((a.n,2)])
 case 12
  a.con = [a.con, np.ones((a.n,1)])

z = a.con(:,12)
a.u = a.con(:,a.ncol)

# at least one angle must be the reference
if sum(z) == 0
  a.con(1,12) = 1
  z(1) = 1
  
# at least one bus must be the slack
if sum(a.u) == 0
  a.u(find(z)) = 1
  a.con(find(z),a.ncol) = 1

DAE.y(a.vbus) = a.con(:,4)
if not sum(DAE.y(Bus.a))  and  a.n == 1
  DAE.y(Bus.a) = a.con(1,5)
else
  DAE.y(a.bus) = a.con(:,5)

# fix reactive power limits
idx = find(a.con(:,6) == 0 & a.con(:,7) == 0)
if not isempty(idx)
  a.con(:,6) =  99*Settings.mva
  a.con(:,7) = -99*Settings.mva
 
# checking the consistency of distributed slack bus
idxpv = pvgamma(PV,'sum')
idxsw = swgamma(a,'sum')
if not idxpv  and  not idxsw, a = setgamma(a); end

a.refbus = a.bus(find(z & a.u))
a.pg = a.con(:,10)
a.dq = np.zeros((a.n,1))
a.qg = np.zeros((a.n,1))
a.qmax = np.ones((a.n,1))
a.qmin = np.ones((a.n,1))
a.store = a.con