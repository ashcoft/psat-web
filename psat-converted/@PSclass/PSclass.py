# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PSclass\PSclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = PSclass(varargin)
# constructor of the class Power System Stabilizer
# == Pss ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.syn = []
  a.exc = []
  a.store = []
  a.va = []
  a.v1 = []
  a.v2 = []
  a.v3 = []
  a.vss = []
  a.omega = []
  a.p = []
  a.vf = []
  a.vref = []
  a.s1 = []
  a.u = []
  a.ncol = 23
  a.format = ['%4d %4d %4d ',repmat('%8.4g ',1,18),'%2u %2u']
  if Settings.matlab, a = class(a,'PSclass'); end
 case 1
  if isa(varargin{1},'PSclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
