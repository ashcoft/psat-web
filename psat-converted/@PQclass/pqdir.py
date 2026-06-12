# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\pqdir.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [p,q] = pqdir(a,idx)  

p = 0
q = 0

if not a.n, return, end

if not isempty(idx)
  p = a.P0(idx)
  q = a.Q0(idx)
