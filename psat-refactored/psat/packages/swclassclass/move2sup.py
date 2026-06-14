# Module: psat.packages.swclassclass.move2sup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = move2sup(a)

if not a.n, return, end

global Supply

idx = find(a.u)
data = np.zeros((a.n,15))
data(:,[1 2 15]) = a.con(:,[1 2 11])
data(:,3) = a.pg
Supply = add(Supply,data(idx,:))
a.pg(idx) = 0