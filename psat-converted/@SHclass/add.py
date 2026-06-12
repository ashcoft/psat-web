# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SHclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = add(a,data)

global Bus

if isempty(data), return, end

n = len(data(:,1))
a.n = a.n + n
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))

m = len(data(1,:))
if  m < a.ncol
  a.u = [a.u; np.ones((n,1)])
  data = [data, np.zeros((n,a.ncol-m)])
else
  a.u = [a.u; data(:,a.ncol)]

a.con = [a.con; data]
