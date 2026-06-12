# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\getbus.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function bus = getbus(a,varargin)

if a.n

  if nargin > 1
    type = varargin{1}
  else
    type = 'angle'
  
  switch type
   case {'voltage','v'}
    bus = a.vbus(find(a.u))
   case {'angle','a'}
    bus = a.bus(find(a.u))
   otherwise
    bus = []

else

  bus = []

