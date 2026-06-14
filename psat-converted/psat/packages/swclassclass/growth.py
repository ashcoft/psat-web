# Module: psat.packages.swclassclass.growth
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function data = growth(a,rr,idx)

data = []

if not a.n, return, end

data = [a.con(:,[1 2]),a.con(:,10).*rr(idx(a.bus)),np.zeros((a.n,16),np.ones((a.n,1)])