# Module: psat.packages.shclassclass.SHclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = SHclass(varargin)
# constructor of the class Shunt
# == Shunt ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.u = []
  a.store = []
  a.ncol = 7
  a.format = ['%4d ',repmat('%8.4g ',1,5),'%2u']
  if Settings.matlab, a = class(a,'SHclass'); end
 case 1
  if isa(varargin{1},'SHclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')