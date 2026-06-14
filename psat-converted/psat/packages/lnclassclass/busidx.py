# Module: psat.packages.lnclassclass.busidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function  b = busidx(a,bus_no)

if not a.n, return, end
if isempty(bus_no), return, end

idx_fr = find(a.fr == bus_no)
idx_to = find(a.to == bus_no)

b = [a.fr(idx_to); a.to(idx_fr)]