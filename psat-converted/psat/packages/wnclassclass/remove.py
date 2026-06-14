# Module: psat.packages.wnclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.n = a.n - len(idx)
a.speed(idx).vw = []
a.speed(idx).time = []
a.vwa(idx) = []
a.vw(idx) = []
a.ws(idx) = []