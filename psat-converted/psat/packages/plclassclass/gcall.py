# Module: psat.packages.plclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

if not a.n, return, end

global DAE Settings

V = DAE.y(a.vbus)

if Settings.init
  DAE.g = DAE.g + ...
          sparse(a.bus,1,DAE.lambda*a.u.*((a.con(:,5).*V+a.con(:,6)).*V+a.con(:,7)),DAE.m,1) + ...
          sparse(a.vbus,1,DAE.lambda*a.u.*((a.con(:,8).*V+a.con(:,9)).*V+a.con(:,10)),DAE.m,1)
elseif not isempty(a.init)
  i = a.init
  DAE.g = DAE.g + ...
          sparse(a.bus(i),1,DAE.lambda*a.u(i).*((a.con(i,5).*V(i)+a.con(i,6)).*V(i)+a.con(i,7)),DAE.m,1) + ...
          sparse(a.vbus(i),1,DAE.lambda*a.u(i).*((a.con(i,8).*V(i)+a.con(i,9)).*V(i)+a.con(i,10)),DAE.m,1)