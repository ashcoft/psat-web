# Module: psat.packages.pvclassclass.PVclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = PVclass(varargin)
# constructor of the class PV
# == PV generator ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.pq = []
  a.qg = []
  a.u = []
  a.store = []
  a.qmax = []
  a.qmin = []
  a.newpq = 0
  a.ncol = 11
  a.format = ['%4d ',repmat('%8.4g ',1,9),'%2u']
  if Settings.matlab, a = class(a,'PVclass'); end
 case 1
  if isa(varargin{1},'PVclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')