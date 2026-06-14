# Module: psat.packages.stclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE

if not a.n, return, end

V = DAE.y(a.vbus)
ist = DAE.x(a.ist)
Kr = a.con(:,5)
Tr = a.con(:,6)

DAE.f(a.ist) = a.u.*(Kr.*(DAE.y(a.vref)-V)-ist)./Tr

# anti-windup limit
fm_windup(a.ist,a.con(:,7),a.con(:,8),'f')