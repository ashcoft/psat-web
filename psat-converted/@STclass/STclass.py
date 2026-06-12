# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@STclass\STclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = STclass(varargin)
# constructor of the class Statcom
# == Statcom ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.ist = []
  a.store = []
  a.vref = []
  a.Vref = []
  a.u = []
  a.ncol = 9
  a.format = ['%4d ', repmat('%8.4g ',1,7),'%2u']
  if Settings.matlab, a = class(a,'STclass'); end
 case 1
  if isa(varargin{1},'STclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
