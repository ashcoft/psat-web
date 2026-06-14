# Module: psat.packages.dmclassclass.pqsum
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def pqsum(a, lambda):

global PQ

if not a.n, return, end

tgd = tanphi(a)

for i in range(1, a.n+1):
  idx = findbus(PQ,a.bus(i))
  pd = lambda*a.u(i)*a.con(i,7)
  qd = lambda*a.u(i)*tgd(i)*a.con(i,7)
  PQ = pqsum(PQ,idx,pd,qd)
