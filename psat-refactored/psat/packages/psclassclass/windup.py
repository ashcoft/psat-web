# Module: psat.packages.psclassclass.windup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def windup(a):

if not a.n, return, end

global DAE

tyb = find(a.con(:,2) > 3)
if isempty(tyb), return, end
vamax = a.con(:,16)
fm_windup(a.va(tyb),vamax(tyb),0,'td')

S2 = a.con(:,22)
S2 = (((DAE.x(a.omega)-1) < 0) | S2) & S2 >= 0
idx = find(S2(tyb))
if isempty(idx), return, end
vathr = a.con(:,17)
fm_windup(a.va(tyb(idx)),vathr(tyb(idx)),0,'td')