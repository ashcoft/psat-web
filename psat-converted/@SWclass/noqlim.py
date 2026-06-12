# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\noqlim.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = noqlim(a,idx)

global Settings

if isnumeric(idx)
  a.con(idx,6) = 999*Settings.mva
  a.con(idx,7) = -999*Settings.mva
elseif strcmp(idx,'all')
  a.con(:,6) = 999*Settings.mva
  a.con(:,7) = -999*Settings.mva
