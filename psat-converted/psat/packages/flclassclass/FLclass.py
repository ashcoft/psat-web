# Module: psat.packages.flclassclass.FLclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = FLclass(varargin)
# constructor of the Frequency Dependent Load
# == Frequency Dependent Load ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.a0 = []
  a.dw = []
  a.x = []
  a.u = []
  a.ncol = 9
  a.format = ['%4d ',repmat('%8.4g ',1,7),'%2u']
  a.store = []
  if Settings.matlab, a = class(a,'FLclass'); end
 case 1
  if isa(varargin{1},'FLclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')