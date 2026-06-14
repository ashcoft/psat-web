# Module: psat.packages.shclassclass.hessian
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function H = hessian(a,ro)
# compute the Hessian matrix of Shunt equations

global DAE

H = sparse(DAE.m,DAE.m)

if not a.n, return, end

H = sparse(a.vbus,a.vbus, ...
           2*a.u.*a.con(:,5).*ro(a.bus) - ...
           2*a.u.*a.con(:,6).*ro(a.vbus), ...
           DAE.m,DAE.m)
