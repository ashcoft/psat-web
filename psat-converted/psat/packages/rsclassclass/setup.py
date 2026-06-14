# Module: psat.packages.rsclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.bus = getint(Bus,a.con(:,1))
if len(a.con(1,:)) < a.ncol
  a.con(:,a.ncol) = np.ones((a.n,1))
a.Pr = np.zeros((a.n,1))
a.u = a.con(:,a.ncol)
a.store = a.con