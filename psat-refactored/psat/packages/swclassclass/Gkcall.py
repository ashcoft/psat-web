# Module: psat.packages.swclassclass.Gkcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gkcall(p):

global DAE

if not p.n, return, end

jdx = find(p.u)
idx = p.bus(jdx)

if isempty(idx),return, end

DAE.Gk(idx) = DAE.Gk(idx) - p.con(jdx,11).*p.pg(jdx)