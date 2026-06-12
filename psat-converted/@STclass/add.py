# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@STclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = add(a,data)

global Bus

a.n = a.n + len(data(1,:))
a.con = [a.con; data]
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))

if len(data(1,:)) < a.ncol
  a.u = [au;np.ones((len(data(1,:)),1)])
else
  a.u = [a.u;data(:,a.ncol)]
