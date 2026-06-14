# Module: psat.packages.suclassclass.pgsum
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def pgsum(a, k):

global PV

if not a.n, return, end

for i in range(1, a.n+1):
  idx = findbus(PV,a.bus(i))
  PV = pvsum(PV,idx,k*a.u(i)*a.con(i,6))
