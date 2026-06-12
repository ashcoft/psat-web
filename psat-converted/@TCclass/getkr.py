# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\getkr.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function kr = getkr(a,idx)

kr = []

if not a.n, return, end
if isempty(idx), return, end

kr = a.u(idx).*a.con(idx,16)
