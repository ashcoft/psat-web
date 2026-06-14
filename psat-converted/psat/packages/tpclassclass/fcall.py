# Module: psat.packages.tpclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(p):

global DAE Settings

if not p.n, return, end

m = DAE.x(p.m)
h = p.u.*p.con(:,4)
k = p.u.*p.con(:,5)

DAE.f(p.m) = -h.*m + k.*(DAE.y(p.vbus)./m - p.con(:,8))

# non-windup limits
fm_windup(p.m,p.con(:,6),p.con(:,7),'pf')