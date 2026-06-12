# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\pvlim.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [qmax,qmin] = pvlim(a)

global Bus

if not a.n
  qmax = []
  qmin = []
  return
qmax = find(Bus.Qg(a.bus) > a.con(:,6) & a.u)
qmin = find(Bus.Qg(a.bus) < a.con(:,7) & a.u)

