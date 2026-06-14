# Module: psat.packages.phclassclass.setup
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

a.n = len(a.con(:,1))
[a.bus1,a.v1] = getbus(Bus,a.con(:,1))
[a.bus2,a.v2] = getbus(Bus,a.con(:,2))

if len(a.con(1,:)) < 15
  a.con = [a.con; np.ones((a.n,1)])

idx = find(a.con(:,15)==0)
if not isempty(idx)
  a.con(idx,15) = 1

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

a.store = a.con

Settings.nseries = Settings.nseries + a.n