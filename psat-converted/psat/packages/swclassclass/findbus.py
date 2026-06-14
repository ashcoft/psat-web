# Module: psat.packages.swclassclass.findbus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = findbus(a,bus)

idx = []
if not a.n, return, end
idx = find(a.bus.*a.u == bus)