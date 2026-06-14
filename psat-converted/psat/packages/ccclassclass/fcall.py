# Module: psat.packages.ccclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(p):

global DAE

if not p.n, return, end

q1 = DAE.x(p.q1)

DAE.f(p.q1) = p.u.*p.con(:,6).*(p.con(:,5)-DAE.y(p.vbus))

# anti-windup limits
fm_windup(p.q1,p.con(:,8),p.con(:,9),'f')