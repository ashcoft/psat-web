# Module: psat.packages.pqclassclass.findgen
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = findgen(a,bus)

idx = []
if not a.n, return, end
idx = find(double(a.bus).*double(a.gen) == bus)