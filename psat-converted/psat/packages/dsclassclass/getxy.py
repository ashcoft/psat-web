# Module: psat.packages.dsclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = getxy(a,bus,x,y)

global Syn

if not a.n, return, end

h = find(ismember(Syn.bus(a.syn),bus))

if not isempty(h)
  x = [x; a.delta_HP(h); a.omega_HP(h); ...
       a.delta_IP(h); a.omega_IP(h); ...
       a.delta_LP(h); a.omega_LP(h); ...
       a.delta_EX(h); a.omega_EX(h)]