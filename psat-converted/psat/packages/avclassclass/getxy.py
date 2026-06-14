# Module: psat.packages.avclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x_temp = [a.vm(h); a.vr1(h); a.vr2(h); a.vr3(h); a.vf(h)]
  idx = find(x_temp)
  x = [x; x_temp(idx)]
  y = [y; a.vref(h)]
