# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CCclass\getxy.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

global Exc Svc Cac

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x = [x; a.q1(h)]
  y = [y; a.q(h)]
