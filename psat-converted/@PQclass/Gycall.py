# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global DAE Settings

if not p.n, return, end
if Settings.forcepq, return, end

vx = p.con(:,6)
vn = p.con(:,7)
z = p.con(:,8).*p.u

a = find((DAE.y(p.vbus) < vn & z) | p.shunt)
b = find(DAE.y(p.vbus) > vx & z)
if not isempty(a)
  h = p.bus(a)
  k = p.vbus(a)
  v2 = vn(a).*vn(a)
  DAE.Gy = DAE.Gy + sparse(h,k,2*p.con(a,4).*DAE.y(k)./v2,DAE.m,DAE.m)
  DAE.Gy = DAE.Gy + sparse(k,k,2*p.con(a,5).*DAE.y(k)./v2,DAE.m,DAE.m)
if not isempty(b)
  h = p.bus(b)
  k = p.vbus(b)
  v2 = vx(b).*vx(b)
  DAE.Gy = DAE.Gy + sparse(h,k,2*p.con(b,4).*DAE.y(k)./v2,DAE.m,DAE.m)
  DAE.Gy = DAE.Gy + sparse(k,k,2*p.con(b,5).*DAE.y(k)./v2,DAE.m,DAE.m)

