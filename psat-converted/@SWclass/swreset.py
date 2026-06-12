# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\swreset.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = swreset(a,idx)

if not a.n, return, end

global Settings

if isnumeric(idx)
  a.pg(idx) = a.store(idx,10).*a.con(:,2)/Settings.mva
elseif strcmp(idx,'all')
  a.pg = a.store(:,10).*a.con(:,2)/Settings.mva
