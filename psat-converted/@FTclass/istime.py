# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FTclass\istime.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function u = istime(a,t)

u = 0

if not a.n, return, end 
if isempty(t), return, end

u = not isempty(find([a.con(:,5);a.con(:,6)] == t(1)))
