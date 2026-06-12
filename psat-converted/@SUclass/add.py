# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\add.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = add(a,data)

global Bus

newbus = getint(Bus,data(:,1))

if len(data(1,:)) < a.ncol
  data(:,a.ncol) = 1

a.n = a.n + len(data(:,1))
a.con = [a.con; data]
a.bus = [a.bus; newbus]
a.u = [a.u; data(:,a.ncol)]
