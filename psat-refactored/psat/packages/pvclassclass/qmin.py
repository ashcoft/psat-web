# Module: psat.packages.pvclassclass.qmin
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [q,idx] = qmin(a)

global Bus Settings

if a.n
  q = a.u.*a.con(:,7)
  idx = a.bus
elseif not isempty(a.store)
  q = a.store(:,a.ncol).*a.store(:,7).*a.store(:,2)/Settings.mva
  idx = getint(Bus,a.store(:,1))
else
  q = []
  idx = []