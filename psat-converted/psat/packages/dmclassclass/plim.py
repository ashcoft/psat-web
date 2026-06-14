# Module: psat.packages.dmclassclass.plim
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [pmax,pmin] = plim(a)

if not a.n
  pmax = []
  pmin = []
  return

pmax = a.u.*a.con(:,5) + 1e-8*(not a.u)
pmin = a.u.*a.con(:,6)