# Module: psat.packages.buclassclass.getarea
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function out = getarea(a,idx,type)

if len(a.con(1,:)) <= 4
  switch type
   case 1
    out = np.ones((len(idx),1))
   case 0
    out = np.ones((a.n,1))
else
  switch type
   case 1
    out = a.con(idx,5)
   case 0 #  all
    out = a.con(:,5)