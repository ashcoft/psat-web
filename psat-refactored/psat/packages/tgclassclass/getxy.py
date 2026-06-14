# Module: psat.packages.tgclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)
# returns indexes to the state and algebraic variables
if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x_temp = [a.tg1(h);a.tg2(h);a.tg3(h);a.tg4(h);a.tg5(h);a.tg(h)]
  idx = find(x_temp)
  x = [x; x_temp(idx)]
  y = [y; a.wref(h)]