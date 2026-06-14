# Module: psat.packages.fcclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x = [x; a.Ik(h); a.Vk(h); a.pH2(h); a.pH2O(h); a.pO2(h); a.qH2(h); a.m(h)]
