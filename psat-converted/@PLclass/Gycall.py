# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PLclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(a):

if not a.n, return, end

global DAE Settings

V = DAE.y(a.vbus)

if Settings.init
  DAE.Gy = DAE.Gy + sparse(a.bus,a.vbus,DAE.lambda*a.u.*(2*a.con(:,5).*V + ...
                             a.con(:,6)),DAE.m,DAE.m)
  DAE.Gy = DAE.Gy + sparse(a.vbus,a.vbus,DAE.lambda*a.u.*(2*a.con(:,8).*V + ...
                             a.con(:,9)),DAE.m,DAE.m)
elseif not isempty(a.init)
  i = a.init
  DAE.Gy = DAE.Gy + sparse( ...
      a.bus(i),a.vbus(i), ...
      DAE.lambda*a.u(i).*(2*a.con(i,5).*V(i)+a.con(i,6)),DAE.m,DAE.m)
  DAE.Gy = DAE.Gy + sparse( ...
      a.vbus(i),a.vbus(i), ...
      DAE.lambda*a.u(i).*(2*a.con(i,8).*V(i)+a.con(i,9)),DAE.m,DAE.m)
