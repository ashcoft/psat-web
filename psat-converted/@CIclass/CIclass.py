# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CIclass\CIclass.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = CIclass(varargin)
# constructor of the class Center of Inertia
# == COI ==

global Settings

switch nargin
 case 0
  a.n = 0
  a.syn = cell(0,0)
  a.M = []
  a.Mtot = []
  a.gen = []
  a.dgen = []
  a.wgen = []
  a.delta = []
  a.omega = []
  if Settings.matlab, a = class(a,'CIclass'); end
 case 1
  if isa(varargin{1},'CIclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')
