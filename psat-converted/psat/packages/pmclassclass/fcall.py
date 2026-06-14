# Module: psat.packages.pmclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

vm = DAE.x(a.vm)
thetam = DAE.x(a.thetam)
V1 = DAE.y(a.vbus)
theta1 = DAE.y(a.bus)

DAE.f(a.vm) = (V1-vm).*a.dat(:,1).*a.u
DAE.f(a.thetam) = (theta1-thetam).*a.dat(:,2).*a.u