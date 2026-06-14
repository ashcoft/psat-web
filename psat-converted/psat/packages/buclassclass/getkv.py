# Module: psat.packages.buclassclass.getkv
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = getkv(a,idx,type)

switch type
 case 1
  out = a.con(idx,2)
 case 2
  out = a.con(idx,2).^2
 case 0 #  all
  out = a.con(:,2)