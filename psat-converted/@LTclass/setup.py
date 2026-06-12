# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LTclass\setup.m  (upstream PSAT, GPL-2.0+)
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

a.n = len(a.con(:,1))
[a.bus1,a.v1] = getbus(Bus,a.con(:,1))
[a.bus2,a.v2] = getbus(Bus,a.con(:,2))

# fix data for backward compatibility
if len(a.con(1,:)) < 17
  a.con = [a.con, 0.5*np.ones((a.n, 1)])
  a.u = np.ones((a.n,1))
elseif len(a.con(1,:)) == 17
  a.u = a.con(:,17)
  a.con(:,17) = 0.5*np.ones((a.n, 1))
else
  a.u = a.con(:,a.ncol)

a.delay = Settings.t0*np.ones((a.n,1))
a.mold = np.ones((a.n,1))
a.store = a.con

# fix remote control bus number
a.vr = a.v2
idx = find(a.con(:,16) == 3)
if not isempty(idx)
  a.vr(idx) = getvint(Bus,a.con(idx,15))

# fix nominal tap ratio
idx = find(a.con(:,6) == 0)
if not isempty(idx)
  a.con(idx,6) = 1

Settings.nseries = Settings.nseries + a.n
