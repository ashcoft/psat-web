# Module: psat.packages.bkclassclass.gettimes
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function t = gettimes(a)

t = []

if not a.n, return, end 

u = unique([a.t1; a.t2])
t = [u-1e-6; u]
