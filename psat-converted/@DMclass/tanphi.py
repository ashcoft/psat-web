# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DMclass\tanphi.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function out = tanphi(a)

out = np.zeros((a.n,1))
idx = find(a.con(:,3) != 0)
if idx
  out(idx) = a.u(idx).*a.con(idx,4)./a.con(idx,3)
