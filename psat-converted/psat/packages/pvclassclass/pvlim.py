# Module: psat.packages.pvclassclass.pvlim
# Refactored from psat-converted
# ------------------------------------------------------------------
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
