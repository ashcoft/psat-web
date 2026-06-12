# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\pvreset.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = pvreset(a,idx)

if not a.n, return, end

global Settings

if isnumeric(idx)
  a.con(idx,4) = a.store(idx,4).*a.con(idx,2)/Settings.mva
elseif strcmp(idx,'all')
  a.con(:,4) = a.store(:,4).*a.con(:,2)/Settings.mva
