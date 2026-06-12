# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DMclass\pqsum.m  (upstream PSAT, GPL-2.0+)
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

