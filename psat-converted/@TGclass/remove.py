# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)
# removes one or more instances of the device
if not a.n, return, end
if isempty(idx), return, end

for i in range(1, len(idx)+1):
  jdx = find(a.ty1 == idx(i))
  if jdx 
    a.ty1(jdx) = []
  jdx = find(a.ty2 == idx(i))
  if jdx 
    a.ty2(jdx) = []
  jdx = find(a.ty3 == idx(i))
  if jdx 
    a.ty3(jdx) = []
  jdx = find(a.ty4 == idx(i))
  if jdx 
    a.ty4(jdx) = []
  jdx = find(a.ty5 == idx(i))
  if jdx 
    a.ty5(jdx) = []
  jdx = find(a.ty6 == idx(i))
  if jdx 
    a.ty6(jdx) = []

a.con(idx,:) = []
a.bus(idx) = []
a.syn(idx) = []
a.tg1(idx) = []
a.tg2(idx) = []
a.tg3(idx) = []
a.tg4(idx) = []
a.tg5(idx) = []
a.tg(idx) = []
a.pm(idx) = []
a.wref(idx) = []
a.u(idx) = []
a.n = a.n - len(idx)
