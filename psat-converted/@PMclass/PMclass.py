# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PMclass\PMclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = PMclass(varargin)
# constructor of the class PMU
# == PMU ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.dat = []
  a.vm = []
  a.thetam = []
  a.u = []
  a.ncol = 6
  a.store = []
  a.format = ['%4d ',repmat('%8.4g ',1,4),' %2u']
  if Settings.matlab, a = class(a,'PMclass'); end
 case 1
  if isa(varargin{1},'PMclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
