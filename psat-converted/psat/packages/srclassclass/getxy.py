# Module: psat.packages.srclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

if not a.n, return, end

h = find(ismember(a.bus,bus))

if not isempty(h)
  x = [x; a.Id(h); a.Iq(h); a.If(h); a.Edc(h); ...
       a.Eqc(h); a.delta(h); a.omega(h); ...
       a.delta_HP(h); a.omega_HP(h); ...
       a.delta_IP(h); a.omega_IP(h); ...
       a.delta_LP(h); a.omega_LP(h); ...
       a.delta_EX(h); a.omega_EX(h)]