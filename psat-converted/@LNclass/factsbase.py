# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\factsbase.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = factsbase(a,idx,Cp,type)

if not a.n, return, end
if isempty(idx), return, end

switch type
 case 'TCSC'
  x = a.u(idx).*Cp./a.con(idx,9)
 case {'SSSC','UPFC'}
  x = a.con(idx,9).*Cp./(1-Cp)

y = a.u(idx).*(1-Cp)./a.con(idx,9)
