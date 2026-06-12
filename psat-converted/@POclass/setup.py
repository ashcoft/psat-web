# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@POclass\setup.m  (upstream PSAT, GPL-2.0+)
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
a.type = a.con(:,3)

a.idx = a.con(:,1)
idx = find(a.type == 1); #  voltage control
if not isempty(idx)
  a.idx(idx) = getvint(Bus,a.con(idx,1))

if len(a.con(1,:)) == a.ncol+1
  a.con = a.con(:,[1:12,14])

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

a.store = a.con


