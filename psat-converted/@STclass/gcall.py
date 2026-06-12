# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@STclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

global DAE

if not a.n, return, end

DAE.g = DAE.g ...
        - sparse(a.vbus,1,a.u.*DAE.x(a.ist).*DAE.y(a.vbus),DAE.m,1) ...
        + sparse(a.vref,1,a.Vref-DAE.y(a.vref),DAE.m,1)
