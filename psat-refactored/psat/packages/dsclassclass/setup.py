# Module: psat.packages.dsclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Syn

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

# machine indexes and parameters
a.syn = a.con(:,1)
a.con(:,18) = 1./getvar(Syn,a.syn,'M')

# the shaft is inactive if the machine is off-line
a.u = a.u.*Syn.u(a.syn)

# setup inverse of inertias
a.con(:,2) = 1./a.con(:,2)
a.con(:,3) = 1./a.con(:,3)
a.con(:,4) = 1./a.con(:,4)
a.con(:,5) = 1./a.con(:,5)

a.store = a.con