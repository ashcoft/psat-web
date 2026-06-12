# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\ybus.m  (upstream PSAT, GPL-2.0+)
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
  if not isempty(jdx)  and  a.u(i), idx = [idx; i]; end

if isempty(idx), return, end

xdb = 0.5*(a.con(idx,10)+a.con(idx,15))
rdb = a.con(idx,7)
zdb = rdb + sqrt(-1)*xdb
ydb = 1/zdb

y = sparse(a.bus(idx),a.bus(idx),ydb,nb,nb)
