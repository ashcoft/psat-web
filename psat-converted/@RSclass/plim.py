# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@RSclass\plim.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [pmax,pmin] = plim(a)

if not a.n
  pmax = []
  pmin = []
  return

pmax = a.u.*a.con(:,3) + 1e-8*(not a.u)
pmin = a.u.*a.con(:,4)
