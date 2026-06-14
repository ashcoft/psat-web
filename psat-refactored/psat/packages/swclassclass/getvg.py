# Module: psat.packages.swclassclass.getvg
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = getvg(a,idx)

p = 0
if not a.n, return, end
if isempty(idx), return, end
if isnumeric(idx)
  p = a.con(idx(find(a.u(idx))),4)
elseif strcmp(idx,'all')
  p = a.con(find(a.u),4)