# Module: psat.packages.oxclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(p):

global DAE

if not p.n, return, end

global DAE

DAE.f(p.v) = p.u.*(DAE.y(p.If) - p.con(:,6))./p.con(:,2)

# anti-windup limit
fm_windup(p.v,p.con(:,7),0,'f')