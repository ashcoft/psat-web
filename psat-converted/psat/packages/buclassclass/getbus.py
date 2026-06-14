# Module: psat.packages.buclassclass.getbus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [u,v] = getbus(a,idx)

u = a.int(round(idx))
v = u + a.n