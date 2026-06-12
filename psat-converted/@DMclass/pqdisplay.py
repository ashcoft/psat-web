# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DMclass\pqdisplay.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = pqdisplay(a)

global PV SW

idx = 0

for i in range(1, a.n+1):
  bpv = findbus(PV,a.u(i)*a.bus(i))
  bsw = findbus(SW,a.u(i)*a.bus(i))
  bdm = a.u(i)*a.con(i,3) > 0
  if isempty(bpv)  and  isempty(bsw)  and  bdm
    idx = a.bus(i)
    break
