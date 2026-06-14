# Module: psat.packages.pqclassclass.PQclass
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = PQclass(varargin)
# constructor of the class PQ
# == PQ load ==

global Settings

switch nargin
 case 0
  a.con = []
  a.n = 0
  a.bus = []
  a.vbus = []
  a.gen = []
  a.store = []
  a.P0 = []
  a.Q0 = []
  a.vmax = []
  a.vmin = []
  a.ncol = 9
  a.shunt = []
  a.u = []
  a.format = ['%4d ',repmat('%8.4g ',1,6),'%2u %2u']
  if Settings.matlab, a = class(a,'PQclass'); end
 case 1
  if isa(varargin{1},'PQclass')
    a = varargin{1}
  else
    error('Wrong argument type')
 otherwise
  error('Wrong Number of input arguments')