# Module: psat.packages.ssclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Line Bus

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.line = a.con(:,1)
a.Cp = a.con(:,6)./100

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

[Line,a.bus1,a.bus2,a.xcs,a.y] = factsetup(Line,a.line,a.u.*a.Cp,'SSSC')

a.v1 = a.bus1 + Bus.n
a.v2 = a.bus2 + Bus.n

a.store = a.con