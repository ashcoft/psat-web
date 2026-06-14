# Module: psat.packages.imclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x_temp = [a.slip(h); a.e1r(h); a.e1m(h); a.e2r(h); a.e2m(h)]
  idx = find(x_temp)
  x = [x; x_temp(idx)]