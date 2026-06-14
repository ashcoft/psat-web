# Module: psat.packages.rlclassclass.RLclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = RLclass(varargin)
# constructor of the class Rmpl
# == Load Ramp ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.dem = []
  a.u = []
  a.store = []
  a.ncol = 9
  a.format = ['%4d ',repmat('%8.4g ',1,7),'%2u']
  if Settings.matlab, a = class(a,'RLclass'); end
 case 1
  if isa(varargin{1},'RLclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')