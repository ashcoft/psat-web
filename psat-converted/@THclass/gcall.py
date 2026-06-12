# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@THclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

global DAE

if not a.n, return, end

T = DAE.x(a.T)
x = DAE.x(a.x)
G = DAE.y(a.G)
V = DAE.y(a.vbus)
Kp = a.con(:,3)
Tref = a.con(:,8)
G_max = a.con(:,9)

DAE.g = DAE.g + sparse(a.bus,1,a.u.*G.*V.^2,DAE.m,1)
DAE.g(a.G) = a.u.*(Kp.*(Tref-T) + x - G)

# windup limits
DAE.y(a.G) = min(DAE.y(a.G),G_max)
DAE.y(a.G) = max(DAE.y(a.G),0)
