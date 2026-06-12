# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DDclass\setup.m  (upstream PSAT, GPL-2.0+)
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
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))
a.wind = round(a.con(:,2))
a.dat = np.zeros((a.n,4))

a.u = np.ones((a.n,1))
if len(a.con(1,:)) <= 25
  a.con(:,25) = 1
else
  a.u = a.con(:,a.ncol)

# fix generator number
a.con(:,25) = round(a.con(:,25))
idx = find(a.con(:,25) <= 0)
if not isempty(idx), a.con(idx,25) = 1; end

a.u = a.u.*fm_genstatus(a.bus)
a.store = a.con
