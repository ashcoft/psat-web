# Module: psat.packages.dmclassclass.add
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = add(a,data)

if isempty(data), return, end

global Bus

if ischar(data)
  data = [1,100,0,0,1e-6,np.zeros((1,12),1])

if len(data(1,:)) < a.ncol
  data(:,a.ncol) = 1

a.con = [a.con; data]
a.n = len(a.con(:,1))
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))
if len(a.con(1,:)) < a.ncol
  a.con(:,a.ncol) = np.ones((a.n,1))
a.u = a.con(:,a.ncol)