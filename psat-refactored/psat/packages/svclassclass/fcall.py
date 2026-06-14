# Module: psat.packages.svclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = fcall(p)

global DAE

if not p.n, return, end

V = DAE.y(p.vbus)
Vref = DAE.y(p.vref)

if not isempty(p.ty1)
  bcv = DAE.x(p.bcv)
  Tr = p.con(p.ty1,6)
  Kr = p.con(p.ty1,7)
  DAE.f(p.bcv) = p.u(p.ty1).*(Kr.*(Vref(p.ty1)-V(p.ty1))-bcv)./Tr
  fm_windup(p.bcv,p.con(p.ty1,9),p.con(p.ty1,10),'f')

if not isempty(p.ty2)
  alpha = DAE.x(p.alpha)
  vm = DAE.x(p.vm)
  T2 = p.con(p.ty2,6)
  K = p.con(p.ty2,7)
  Kd = p.con(p.ty2,11)
  T1 = p.con(p.ty2,12)
  Km = p.con(p.ty2,13)
  Tm = p.con(p.ty2,14)
  xl = p.con(p.ty2,15)
  xc = p.con(p.ty2,16)
  DAE.f(p.vm) = p.u(p.ty2).*(Km.*V(p.ty2)-vm)./Tm
  DAE.f(p.alpha) = p.u(p.ty2).*(-Kd./T2.*alpha+K.*T1./T2./Tm.*(vm-Km.*V(p.ty2))+K./T2.*(Vref(p.ty2)-vm))
  fm_windup(p.alpha,p.con(p.ty2,9),p.con(p.ty2,10),'f')

p.Be = bsvc(p)