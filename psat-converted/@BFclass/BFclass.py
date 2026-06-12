# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BFclass\BFclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = BFclass(varargin)
# constructor of the class Busfreq
# == Busfreq ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.dat = []
  a.x = []
  a.w = []
  a.u = []
  a.ncol = 4
  a.store = []
  a.format = ['%4d %8.4g %8.4g %2u']
  if Settings.matlab, a = class(a,'BFclass'); end
 case 1
  if isa(varargin{1},'BFclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
