# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DMclass\pqset.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pqset(a,tanphi)

if not a.n, return, end
a.con(:,3) = a.u.*a.con(:,7)
a.con(:,4) = a.u.*a.con(:,7).*tanphi
