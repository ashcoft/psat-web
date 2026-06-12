# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\setup.m  (upstream PSAT, GPL-2.0+)
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
a.ty1 = find(a.con(:,2) == 1)
a.ty2 = find(a.con(:,2) == 2)
a.Cp = a.con(:,8)./100

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

[Line,a.bus1,a.bus2,a.B,a.y] = factsetup(Line,a.line,a.u.*a.Cp,'TCSC')

a.v1 = a.bus1 + Bus.n
a.v2 = a.bus2 + Bus.n

a.store = a.con
