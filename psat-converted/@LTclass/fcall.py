# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LTclass\fcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fcall(p):

global DAE 

if not p.n, return, end

mc = DAE.x(p.mc)
md = DAE.y(p.md)

h = p.con(:,7)
k = p.con(:,8)
mmax = p.con(:,9)
mmin = p.con(:,10)
ref = p.con(:,12)
ctype = p.con(:,16)

error = np.zeros((p.n,1))
ty1 = find(ctype == 1 | ctype == 3)
ty2 = find(ctype == 2)

if ty1
  error(ty1) = DAE.y(p.vr(ty1))-ref(ty1)
if ty2
  Vf = p.u.*DAE.y(p.v1).*exp(i*DAE.y(p.bus1))
  Vt = p.u.*DAE.y(p.v2).*exp(i*DAE.y(p.bus2))
  y = admittance(p)
  q2 = imag(Vt.*conj((Vt-Vf./md).*y))
  error(ty2) = -ref(ty2)-q2(ty2)

DAE.f(p.mc) = p.u.*(k.*error-h.*mc)
#disp([md, mc, DAE.g(p.md), DAE.f(p.mc), DAE.g(p.v1), ...
#      DAE.g(p.v2), DAE.g(p.bus1), DAE.g(p.bus2)])

# non-windup limits
fm_windup(p.mc, mmax, mmin, 'pf')

