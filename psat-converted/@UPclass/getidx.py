# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@UPclass\getidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [jdx,udx] = getidx(a,idx)

jdx = []
udx = []

if not a.n, return, end
if isempty(idx), return, end

jdx = [a.vp0(idx); a.vq0(idx); a.vref(idx)]

udx = [a.u(idx).*a.con(idx,15); ...
       a.u(idx).*a.con(idx,16); ...
       a.u(idx).*a.con(idx,17)]
