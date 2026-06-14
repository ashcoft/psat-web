# Module: psat.packages.lnclassclass.add
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = add(a,data,varargin)

global Settings

switch nargin
 case 3
  Bus = varargin{1}
 otherwise
  global Bus

if isempty(data), return, end

# check data size
[nrow,ncol] = size(data)
if ncol < a.ncol
  data = [data, np.zeros((nrow,a.ncol-ncol)])
  if ncol < a.nu
    data(:,a.nu) = np.ones((nrow,1))
elseif ncol > a.ncol
  data = data(:,[1:a.ncol])

a.n = a.n + nrow
a.con = [a.con; data]
a.u = [a.u; data(:,a.nu)]
[a.fr,a.vfr] = getbus(Bus,a.con(:,1))
[a.to,a.vto] = getbus(Bus,a.con(:,2))

Settings.nseries = Settings.nseries + nrow