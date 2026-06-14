# Module: psat.packages.rsclassclass.add
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = add(a,data)

global Bus

newbus = getint(Bus,data(:,1))

if len(data(1,:)) < a.ncol
  data(:,a.ncol) = 1

a.n = a.n + len(data(:,1))
a.con = [a.con; data]
a.bus = [a.bus; newbus]
a.Pr = [a.Pr; np.zeros((len(data(:,1)),1)])
a.u = [a.u; data(:,a.ncol)]