# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\synsat.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function output = synsat(a,flag,e1q,isx)

b = [0.8*np.ones((len(isx),1), 1-a.con(isx,25), 1.2*(1-a.con(isx,26))])
c2 = b*[12.5; -25; 12.5]
c1 = b*[-27.5; 50; -22.5]
c0 = b*[15; -24; 10]

switch flag

 case 1 #  saturation function
  
  output = e1q
  idx = find(output > 0.8)
  if not isempty(idx)
    output(idx)=(c2(idx).*e1q(idx)+c1(idx)).*e1q(idx)+c0(idx)
# idx2 = idx(e1q(idx) > -c1(idx)./(2*c2(idx)));
# if ~isempty(idx2)
#   output(idx2) = (-c2(idx2).*c1(idx2).^2+4*c2(idx2).^2.* ...
#                   c0(idx2))./(4*c2(idx2).^2);
# end
  
 case 2 #  Jacobian
  
  output = np.ones((len(isx),1))
  idx = find(e1q > 0.8)
  if not isempty(idx)
    output(idx)=2*c2(idx).*e1q(idx) + c1(idx)
# idx2 = idx(e1q(idx) > -c1(idx)./(2*c2(idx)));
# if ~isempty(idx2)
#   output(idx2) = 0;
# end
  
