# Module: psat.packages.tpclassclass.restore
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = restore(a)

if isempty(a.store)
  a = init(a)
else
  a.con = a.store
  a = setup(a)