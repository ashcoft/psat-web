# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LTclass\flows.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [Ps,Qs,Pr,Qr,varargout] = flows(a,Ps,Qs,Pr,Qr,varargin)

global DAE

if nargin == 7
  varargout{1} = [varargin{1}; a.bus1]
  varargout{2} = [varargin{2}; a.bus2]

if not a.n, return, end

Vf = a.u.*DAE.y(a.v1).*exp(i*DAE.y(a.bus1))
Vt = a.u.*DAE.y(a.v2).*exp(i*DAE.y(a.bus2))
y = admittance(a)
m = DAE.y(a.md)

Ss = Vf.*conj((Vf./m-Vt).*y./m)
Sr = Vt.*conj((Vt-Vf./m).*y)

Ps = [Ps; real(Ss)]
Qs = [Qs; imag(Ss)]
Pr = [Pr; real(Sr)]
Qr = [Qr; imag(Sr)]
