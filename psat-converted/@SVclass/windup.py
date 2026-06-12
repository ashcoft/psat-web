# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SVclass\windup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def windup(a):

if not a.n, return, end

if a.ty1, fm_windup(a.bcv,a.con(a.ty1,9),a.con(a.ty1,10),'td'), end
if a.ty2, fm_windup(a.alpha,a.con(a.ty2,9),a.con(a.ty2,10),'td'), end
