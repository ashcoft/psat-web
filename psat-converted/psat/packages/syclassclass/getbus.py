# Module: psat.packages.syclassclass.getbus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function bus = getbus(a,varargin)

bus = []

if not a.n, return, end

if nargin > 1
  idx = varargin{1}
  if isempty(idx), return, end
  bus = a.bus(idx)
else
  bus = a.bus(find(a.u))