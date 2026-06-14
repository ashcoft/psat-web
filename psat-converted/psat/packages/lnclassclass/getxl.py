# Module: psat.packages.lnclassclass.getxl
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function xl = getxl(a,idx)

xl = []

if not a.n, return, end
if isempty(idx), return, end

xl = a.con(idx,9)