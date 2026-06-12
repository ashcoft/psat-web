# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\move2sw.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function data = move2sw(a)

global DAE

[amax,idx] = max(a.u.*a.con(:,4))
data = [a.con(idx,[1 2 3 5]), ...
        DAE.y(a.bus(idx)), ...
        a.con(idx,[6 7 8 9 4 10]), 0, 1]
a = remove(a,idx)
