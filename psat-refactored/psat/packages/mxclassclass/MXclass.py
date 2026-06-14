# Module: psat.packages.mxclassclass.MXclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = MXclass(varargin)
# constructor of the Mixed Load
# == Mixed Load ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.dat = []
  a.x = []
  a.y = []
  a.u = []
  a.ncol = 15
  a.format = ['%4d ',repmat('%8.4g ',1,13),'%2u']
  a.store = []
  if Settings.matlab, a = class(a,'MXclass'); end
 case 1
  if isa(varargin{1},'MXclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')