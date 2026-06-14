# Module: psat.packages.svclassclass.remove
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
    a.bcv(jdx,:) = []
  jdx = find(a.ty2 == idx(i))
  if jdx
    a.ty2(jdx) = []
    a.alpha(jdx,:) = []
    a.vm(jdx,:) = []

a.con(idx,:) = []
a.bus(idx) = []
a.vbus(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)
a.Be(idx,:) = []
a.vref(idx,:) = []
a.q(idx,:) = []