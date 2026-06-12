# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)
# initializes the main devices properties using the property con
global Syn 

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.syn = a.con(:,1)
a.bus = getbus(Syn,a.syn)

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)
# the TG is inactive if the machine is off-line
a.u = a.u.*Syn.u(a.syn)

a.store = a.con
