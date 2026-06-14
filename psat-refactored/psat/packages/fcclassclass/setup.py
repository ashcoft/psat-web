# Module: psat.packages.fcclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
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

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)
a.u = a.u.*fm_genstatus(a.bus)

# RTon2F
a.con(:,20) = 0.5*8.314*a.con(:,20)/96487

a.store = a.con