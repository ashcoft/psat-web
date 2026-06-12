# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@MNclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

if not a.n, return, end

global Settings

if not isempty(a.init)
  k = a.init
  a.con(k,4) = a.con(k,4).*a.con(k,2)/Settings.mva
  a.con(k,5) = a.con(k,5).*a.con(k,2)/Settings.mva
