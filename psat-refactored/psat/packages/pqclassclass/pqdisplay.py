# Module: psat.packages.pqclassclass.pqdisplay
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = pqdisplay(a)

global PV SW

idx = 0

for i in range(1, a.n+1):
  bpv = findbus(PV,a.bus(i))
  bsw = findbus(SW,a.bus(i))
  bpq = a.u(i)*a.con(i,4) > 0
  if isempty(bpv)  and  isempty(bsw)  and  bpq
    idx = a.bus(i)
    break