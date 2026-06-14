# Module: psat.packages.avclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Syn Bus

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.syn = a.con(:,1)
a.bus = getbus(Syn,a.syn)
a.vbus = a.bus + Bus.n

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)
# the AVR is inactive if the machine is off-line
a.u = a.u.*Syn.u(a.syn)

a.store = a.con