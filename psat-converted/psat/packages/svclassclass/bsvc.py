# Module: psat.packages.svclassclass.bsvc
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function B = bsvc(a)

global DAE

B = np.zeros((a.n,1))

if a.ty1
  B(a.ty1) = DAE.x(a.bcv)

if a.ty2
  xl = a.con(a.ty2,15)
  xc = a.con(a.ty2,16)
  B(a.ty2) = (2*DAE.x(a.alpha) - sin(2*DAE.x(a.alpha)) ...
              - np.pi*(2-xl./xc))./(np.pi*xl)