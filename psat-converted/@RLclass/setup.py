# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@RLclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Demand

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.dem = round(a.con(:,1))
a.bus = Demand.bus(a.dem)
if len(a.con(1,:)) < a.ncol
  a.con(:,a.ncol) = np.ones((a.n,1))
a.u = a.con(:,a.ncol)
a.store = a.con
