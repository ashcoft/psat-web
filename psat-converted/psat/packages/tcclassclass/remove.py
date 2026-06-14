# Module: psat.packages.tcclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

for i in range(1, len(idx)+1):
  jdx = find(a.ty1 == idx(i))
  if jdx 
    a.ty1(jdx) = []
  jdx = find(a.ty2 == idx(i))
  if jdx 
    a.ty2(jdx) = []
    a.x2(jdx) = []

a.con(idx,:) = []
a.bus1(idx) = []
a.bus2(idx) = []
a.v1(idx) = []
a.v2(idx) = []
a.line(idx) = []
a.n = a.n - len(idx)
a.x1(idx,:) = []
a.B(idx,:) = []
a.Cp(idx,:) = []
a.X0(idx,:) = []
a.Pref(idx,:) = []
a.x0(idx,:) = []
a.pref(idx,:) = []
a.y(idx,:) = []
a.u(idx) = []