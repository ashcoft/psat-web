# Module: psat.packages.mnclassclass.getnum
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function n = getnum(a)

if a.n
  n = sum(not a.con(:,8).*a.u)
else
  n = 0