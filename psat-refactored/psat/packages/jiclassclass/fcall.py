# Module: psat.packages.jiclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

x = DAE.x(a.x)
V1 = DAE.y(a.vbus)
iTf = a.u./a.con(:,5)

DAE.f(a.x) = -(V1.*iTf+x).*iTf