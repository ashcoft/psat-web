# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\flows.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [Ps,Qs,Pr,Qr] = flows(a,Ps,Qs,Pr,Qr,varargin)

global DAE

if not a.n, return, end

if nargin == 5
  type = 'all'
else
  type = varargin{1}

# update B
B = btcsc(a)

V1 = DAE.y(a.v1)
V2 = DAE.y(a.v2)
ss = sin(DAE.y(a.bus1)-DAE.y(a.bus2))
cc = cos(DAE.y(a.bus1)-DAE.y(a.bus2))

P1 = V1.*V2.*ss.*B

switch type
 case 'all'
  Ps(a.line) = Ps(a.line) + P1
  Pr(a.line) = Pr(a.line) - P1
  Qs(a.line) = Qs(a.line) + V1.*(V1-V2.*cc).*B
  Qr(a.line) = Qr(a.line) + V2.*(V2-V1.*cc).*B
 case 'tcsc'
  Ps = Ps + P1
  Pr = Pr - P1
  Qs = Qs + V1.*(V1-V2.*cc).*B
  Qr = Qr + V2.*(V2-V1.*cc).*B
