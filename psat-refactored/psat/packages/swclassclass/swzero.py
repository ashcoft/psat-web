# Module: psat.packages.swclassclass.swzero
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = swzero(a,idx)

if not a.n, return, end
if isnumeric(idx)
  a.pg(idx) = 0
elseif strcmp(idx,'all')
  a.pg = np.zeros((a.n,1))