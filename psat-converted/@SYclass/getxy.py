# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\getxy.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x_temp = [a.delta(h); a.omega(h); a.e1q(h); a.e1d(h); ...
       a.e2q(h); a.e2d(h); a.psiq(h); a.psid(h)]
  idx = find(x_temp)
  x = [x; x_temp(idx)]
  y = [y; a.vf(h); a.pm(h); a.p(h); a.q(h)]
