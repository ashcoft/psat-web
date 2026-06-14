# Module: psat.packages.lsclassclass.getnum
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function n = getnum(a)

if a.n
  n = sum(a.u)
else
  n = 0