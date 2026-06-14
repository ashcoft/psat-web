# Module: psat.packages.ftclassclass.gettimes
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function t = gettimes(a)

t = []

if not a.n, return, end 

u = unique([a.con(:,5); a.con(:,6)])
t = [u-1e-6; u]