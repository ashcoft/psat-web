# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\qmax.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [q,idx] = qmax(a)

global Bus Settings

if a.n
  q = a.u.*a.con(:,6)
  idx = a.bus
elseif not isempty(a.store)
  q = a.store(:,a.ncol).*a.store(:,6).*a.store(:,2)/Settings.mva
  idx = getint(Bus,a.store(:,1))
else
  q = []
  idx = []
