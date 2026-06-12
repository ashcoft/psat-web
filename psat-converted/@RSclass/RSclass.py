# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@RSclass\RSclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = RSclass(varargin)
# constructor of the class Rsrv
# == Generator Reserve ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.u = []
  a.Pr = []
  a.store = []
  a.ncol = 6
  a.format = ['%4d ',repmat('%8.4g ',1,4),'%2u']
  if Settings.matlab, a = class(a,'RSclass'); end
 case 1
  if isa(varargin{1},'RSclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
