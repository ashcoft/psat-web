# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ELclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

V = DAE.y(a.vbus)
P0 = a.dat(:,1)
Q0 = a.dat(:,2)
V0 = a.dat(:,3)

DAE.f(a.xp) = -a.u.*(DAE.x(a.xp)./a.con(:,5) - ...
                     P0.*(V./V0).^a.con(:,7) + ...
                     P0.*(V./V0).^a.con(:,8))
DAE.f(a.xq) = -a.u.*(DAE.x(a.xq)./a.con(:,6) - ...
                     Q0.*(V./V0).^a.con(:,9) + ...
                     Q0.*(V./V0).^a.con(:,10))
