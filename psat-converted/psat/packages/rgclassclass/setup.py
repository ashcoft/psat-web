# Module: psat.packages.rgclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Supply

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.sup = round(a.con(:,1))
a.bus = Supply.bus(a.sup)
if len(a.con(1,:)) < a.ncol
  a.con(:,a.ncol) = np.ones((a.n,1))
a.u = a.con(:,a.ncol)
a.store = a.con