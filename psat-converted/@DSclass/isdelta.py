# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DSclass\isdelta.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = isdelta(a,idx)

global Settings

out = 0

if not a.n, return, end

if Settings.hostver > 7
  out1 = not isempty(find(a.delta_HP == idx,1))
  out2 = not isempty(find(a.delta_IP == idx,1))
  out3 = not isempty(find(a.delta_LP == idx,1))
  out4 = not isempty(find(a.delta_EX == idx,1))
else
  out1 = not isempty(find(a.delta_HP == idx))
  out2 = not isempty(find(a.delta_IP == idx))
  out3 = not isempty(find(a.delta_LP == idx))
  out4 = not isempty(find(a.delta_EX == idx))

out = out1  or  out2  or  out3  or  out4
