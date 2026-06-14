# Module: psat.packages.bkclassclass.istime
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function u = istime(a,t)

u = 0

if not a.n, return, end 
if isempty(t), return, end

u = not isempty(find([a.t1; a.t2] == t(1)))