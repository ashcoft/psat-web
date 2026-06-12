# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@RGclass\RGclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = RGclass(varargin)
# constructor of the class Rmpg
# == Generator Ramp ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.sup = []
  a.u = []
  a.store = []
  a.ncol = 10
  a.format = '%4d %8.4g %8.4g %8.4g %4d %4d %4d %4d %8.4g %2u'
  if Settings.matlab, a = class(a,'RGclass'); end
 case 1
  if isa(varargin{1},'RGclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
