# Module: psat.packages.ltclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h1 = ismember(a.bus1,bus)
h2 = ismember(a.bus2,bus)
h = find(h1+h2)

if not isempty(h)
  x = [x; a.mc(h)]
  y = [y; a.md(h)]