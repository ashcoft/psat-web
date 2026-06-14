# Module: psat.packages.pvclassclass.move2sup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = move2sup(a,idx)

if not a.n, return, end

global Supply

if isempty(idx), return, end

data = np.zeros((len(idx),15))
data(:,[1 2 3 15]) = a.con(idx,[1 2 4 10])
Supply = add(Supply,data)

a = remove(a,idx)