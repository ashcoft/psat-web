# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\CLclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = CLclass(varargin)
# constructor of the class Cluster
# == Cluster ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.q = []
  a.syn = []
  a.exc = []
  a.svc = []
  a.vref = []
  a.cac  = []
  a.Vs = []
  a.dVsdQ = []
  a.u = []
  a.store = []
  a.ncol = 10
  a.format = ['%4d %4d %4d ',repmat('%8.4g ',1,6),'%2u']
  if Settings.matlab, a = class(a,'CLclass'); end
 case 1
  if isa(varargin{1},'CLclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
