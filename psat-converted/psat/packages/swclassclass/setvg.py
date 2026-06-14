# Module: psat.packages.swclassclass.setvg
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setvg(a,idx,v)

if not a.n, return, end
if isempty(idx), return, end
if isnumeric(idx)
  a.con(idx,4) = v
elseif strcmp(idx,'all')
  a.con(:,4) = v