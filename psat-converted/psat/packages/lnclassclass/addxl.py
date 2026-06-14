# Module: psat.packages.lnclassclass.addxl
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = addxl(a,idx,val)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,9) = a.con(idx,9) + val