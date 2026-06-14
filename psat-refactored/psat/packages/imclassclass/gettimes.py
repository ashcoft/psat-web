# Module: psat.packages.imclassclass.gettimes
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function t = gettimes(a)

t = []

if not a.n, return, end 

u = unique(a.con(:,18).*(not a.z).*a.u)
u(find(u == 0)) = []
if isempty(u)
  t = []
else
  t = [u-1e-6; u]