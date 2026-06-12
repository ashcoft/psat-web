# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\balpha.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function out = balpha(p,af,idx,type)

xC = p.con(p.ty2(idx),15)
xL = p.con(p.ty2(idx),14)

switch type
 case 1
  kx1 = sqrt(xC./xL)
  kx2 = kx1.*kx1
  kx3 = kx2.*kx1
  kx4 = kx3.*kx1
  ckf = cos(kx1.*(np.pi-af))
  skf = sin(kx1.*(np.pi-af))
  s2a = sin(2*af)
  caf = cos(af)
  saf = sin(af)
  out = (np.pi*(kx4-2*kx2+1).*ckf)./(xC.*((np.pi*kx4-np.pi-2*kx4.*af+2*af.*kx2- ...
      kx4.*s2a+kx2.*s2a-4*kx2.*caf.*saf).*ckf -4*kx3.*caf.*caf.*skf))
 case 2
  kx1 = sqrt(xC./xL)
  kx2 = kx1.*kx1
  kx3 = kx2.*kx1
  kx4 = kx3.*kx1
  ckf = cos(kx1.*(-np.pi+af))
  skf = sin(kx1.*(-np.pi+af))
  ck2 = ckf.*ckf
  c2a = cos(2*af)
  s2a = sin(2*af)
  caf = cos(af)
  saf = sin(af)
  ca2 = caf.*caf
  out = 2*np.pi*(-kx4+2*kx2-1).*(2*skf.*skf.*kx1.*kx3.*ca2-ck2.*kx4+ck2.*kx2- ...
      ck2.*kx4.*c2a+ck2.*kx2.*c2a+2*ck2.*kx2.*saf.*saf-2*ck2.*kx2.*ca2- ...
      4*ckf.*kx3.*caf.*skf.*saf+2*kx3.*ca2.*ck2.*kx1)./xC./(ckf.*np.pi.*kx4- ...
      ckf.*np.pi-2*ckf.*kx4.*af+2*ckf.*af.*kx2-ckf.*kx4.*s2a+ckf.*kx2.*s2a- ...
      4*ckf.*kx2.*caf.*saf+4*kx3.*ca2.*skf).^2
