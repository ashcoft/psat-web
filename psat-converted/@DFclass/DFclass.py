# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DFclass\DFclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = DFclass(varargin)
# constructor of the class Doubly-Fed Induction Generator
# == DFIG ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.wind = []
  a.dat = []
  a.omega_m = []
  a.theta_p = []
  a.idr = []
  a.iqr = []
  a.vref = []
  a.pwa = []
  a.store = []
  a.u = []
  a.ncol = 25
  a.format = ['%4d %4d ',repmat('%8.4g ',1,21),'%2u %2u']
  if Settings.matlab, a = class(a,'DFclass'); end
 case 1
  if isa(varargin{1},'DFclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
