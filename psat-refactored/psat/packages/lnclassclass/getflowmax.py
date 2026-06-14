# Module: psat.packages.lnclassclass.getflowmax
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = getflowmax(a,type)

global Settings

out = []

if not a.n, return, end

switch type
 case {'imax',1}
  out = a.con(:,13)
 case {'pmax',2}
  out = a.con(:,14)
 case {'smax',3}
  out = a.con(:,15)

idx = find(out <= 0)
if not isempty(idx)
  out(idx) = 1e6*Settings.mva