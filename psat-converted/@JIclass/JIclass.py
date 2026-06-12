# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@JIclass\JIclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = JIclass(varargin)
# constructor of the Jimma Load
# == Jimma Load ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.dat = []
  a.x = []
  a.u = []
  a.ncol = 13
  a.format = ['%4d ',repmat('%8.4g ',1,11),'%2u']
  a.store = []
  if Settings.matlab, a = class(a,'JIclass'); end
 case 1
  if isa(varargin{1},'JIclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
