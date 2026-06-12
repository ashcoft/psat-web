# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = gcall(a)

global Bus DAE

if not a.n, return, end

DAE.g = np.zeros((DAE.m,1))

na = Bus.a
nv = Bus.v

DAE.y(nv) = max(DAE.y(nv),1e-6)
Vc = DAE.y(nv).*exp(i*DAE.y(na))
S = Vc.*conj(a.Y*Vc)
a.p = real(S)
a.q = imag(S)

DAE.g(na) = a.p
DAE.g(nv) = a.q

