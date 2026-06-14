# Module: psat.packages.flclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = fcall(a)

global DAE

if not a.n, return, end

DAE.f(a.x) = -a.u.*DAE.y(a.dw)./a.con(:,8)