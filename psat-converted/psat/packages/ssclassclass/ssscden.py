# Module: psat.packages.ssclassclass.ssscden
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function den = ssscden(a)

global DAE

V1 = DAE.y(a.v1)
V2 = DAE.y(a.v2)
cc = cos(DAE.y(a.bus1)-DAE.y(a.bus2))

den = max(sqrt(V1.^2+V2.^2-2.*V1.*V2.*cc),1e-6*np.ones((a.n,1))