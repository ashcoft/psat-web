# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

global Settings

if not a.n, return, end

a.con(:,4) = a.con(:,3).*a.con(:,4)/Settings.mva
a.con(:,5) = a.con(:,3).*a.con(:,5)/Settings.mva
a.con(:,7) = a.con(:,3).*a.con(:,7)/Settings.mva
a.con(:,8) = a.con(:,3).*a.con(:,8)/Settings.mva

