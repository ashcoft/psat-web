# Module: psat.packages.pqclassclass.pqsub
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pqsub(a,idx,p,q)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,4) = a.con(idx,4) - p
a.con(idx,5) = a.con(idx,5) - q