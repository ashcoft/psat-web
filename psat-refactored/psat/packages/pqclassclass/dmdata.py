# Module: psat.packages.pqclassclass.dmdata
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function data = dmdata(a,idx)

global Bus

data = np.zeros((1,17))
data(1) = getidx(Bus,1)

if not a.n, return, end

data = np.zeros((len(idx),17))
data(:,[1 2]) = a.con(idx,[1 2])
data(:,3) = a.u(idx).*a.con(idx,4)
data(:,4) = a.u(idx).*a.con(idx,5)
data(:,14) = 1