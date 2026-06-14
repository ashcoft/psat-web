# Module: psat.packages.shclassclass.ybus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function y = ybus(a,buslist)

global Bus

nb = Bus.n
y = sparse(nb,nb)

if not a.n, return, end

idx = []
for i = 1:a.n,
  jdx = find(buslist != a.bus(i))
  if not isempty(jdx)  and  a.u(i), 
    idx = [idx; i]

if isempty(idx), return, end

y = sparse(a.bus(idx),a.bus(idx),a.con(idx,5)+sqrt(-1)*a.con(idx,6),nb,nb)