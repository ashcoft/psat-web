# Module: psat.packages.buclassclass.sortbus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [buses,idxes] = sortbus(a,maxn)

[buses,idxes] = sort(a.names(1:min(a.n,maxn)))