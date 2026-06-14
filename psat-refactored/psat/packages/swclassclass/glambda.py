# Module: psat.packages.swclassclass.glambda
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda, kg):

global DAE

if not p.n, return, end

jdx = find(p.u)
idx = p.bus(jdx)

if isempty(idx),return, end

DAE.g(idx) = DAE.g(idx) - (lambda+kg*p.con(jdx,11)).*p.pg(jdx)
