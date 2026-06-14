# Module: psat.packages.ddclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
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
  x = [x; a.theta_p(h); a.omega_m(h); a.iqs(h); a.idc(h); vw]
  y = [y; a.ids(h); a.iqc(h); a.pwa(h); ws]