# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PLclass\PLclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = PLclass(varargin)
# constructor of the Polinomial Load
# == Polinomial Load ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.init = []
  a.u = []
  a.store = []
  a.ncol = 12
  a.format = ['%4d ',repmat('%8.4g ',1,9),'%2u %2u']
  if Settings.matlab, a = class(a,'PLclass'); end
 case 1
  if isa(varargin{1},'PLclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
