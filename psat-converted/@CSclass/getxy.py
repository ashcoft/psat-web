# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CSclass\getxy.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

global Wind

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  vw = Wind.vw(a.wind(h))
  ws = Wind.ws(a.wind(h))
  x = [x; a.omega_t(h); a.omega_m(h); a.gamma(h); a.e1r(h); a.e1m(h); vw]
  y = [y; ws]
