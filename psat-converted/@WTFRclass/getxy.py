# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WTFRclass\getxy.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

global Dfig

h = ismember(Dfig.bus(a.gen),bus)

if not isempty(h)
  x = [x; a.Dfm(h); a.x(h); a.csi(h); a.pfw(h)]
  y = [y; a.pf1(h); a.pwa(h)]
