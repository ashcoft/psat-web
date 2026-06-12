# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@OXclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus Exc Syn

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.exc = a.con(:,1)
a.syn = Exc.syn(a.exc)
a.bus = getbus(Syn,a.syn)
a.vbus = a.bus + Bus.n

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)
# the OXL is inactive if the AVR is off-line
a.u = a.u.*Exc.u(a.exc)

a.store = a.con
