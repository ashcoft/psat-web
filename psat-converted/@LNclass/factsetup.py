# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\factsetup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [a,bus1,bus2,x,y] = factsetup(a,idx,Cp,type)

if not a.n, return, end
if isempty(idx), return, end

bus1 = a.fr(idx)
bus2 = a.to(idx)
y = a.u(idx)./a.con(idx,9)

# neglect line resistance, charging and tap ratio
jdx = find(Cp)
if not isempty(Cp)
  a.con(idx(jdx),[8 10 12]) = 0
  a.con(idx(jdx),11) = 1

switch type
 case 'TCSC'
  x = a.u(idx).*Cp./a.con(idx,9)./(1-Cp)
  a.con(idx,9) = (1-Cp).*a.con(idx,9)
 case {'SSSC','UPFC'}
  x = Cp.*a.con(idx,9)
  a.con(idx,9) = a.con(idx,9) - x
