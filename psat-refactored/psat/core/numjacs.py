# Module: psat.core.numjacs
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

fm_call('i')

ffn = DAE.f
ggn = DAE.g
xa  = DAE.x
ya  = DAE.y
tol = 1e-8

Gx = np.zeros((DAE.m,DAE.n))
Fx = np.zeros((DAE.n,DAE.n))
Gy = np.zeros((DAE.m,DAE.m))
Fy = np.zeros((DAE.n,DAE.m))

black_list = [Ddsg.theta_p; Dfig.theta_p; Oxl.v; Hvdc.xi]

for j = 1:DAE.m

  deltaa = max(tol,abs(tol*DAE.y(j)))
  DAE.y(j)=DAE.y(j)+deltaa
  
  fm_call('i')

  if DAE.n, Fy(:,j)=(DAE.f-ffn)./deltaa; end
  Gy(:,j)=(DAE.g-ggn)./deltaa

  DAE.x  = xa
  DAE.y  = ya


fm_call('i')

for j = 1:DAE.n

  deltaX = max(tol,abs(tol*DAE.x(j)))
  Xinc = deltaX
  if not isempty(black_list)
    if not isempty(find(black_list == j))
      Xinc = 0
  DAE.x(j)=DAE.x(j)+Xinc
  
  fm_call('i')

  Fx(:,j)=(DAE.f-ffn)./deltaX
  Gx(:,j)=(DAE.g-ggn)./deltaX

  DAE.x  = xa
  DAE.y  = ya


Sbus = getbus(SW)
Gbus = [getbus(SW,'v');getbus(PV,'v')]

if not DAE.n
  Fx = 1
  Gx = np.zeros((DAE.m,1))
  Fy = np.zeros((1,DAE.m))

if not isempty(black_list)
for i in range(1, len(black_list)+1):
    k = black_list(i)
    Fx(k,k) = DAE.Fx(k,k)

for i in range(1, len(Hvdc.cosg)+1):
  k = Hvdc.cosg(i)
  Gy(k,k) = DAE.Gy(k,k)
  k = Hvdc.xi(i)
  h = Hvdc.yi(i)
  Fy(k,h) = DAE.Fy(k,h)
  k = Hvdc.xr(i)
  h = Hvdc.yr(i)
  Fy(k,h) = DAE.Fy(k,h)

Gy(Gbus,:) = 0
Gy(:,Gbus) = 0
Gy(Gbus,Gbus) = np.eye(getnum(PV)+getnum(SW))
Gy(:,Sbus) = 0
Gy(Sbus,:) = 0
Gy(Sbus,Sbus) = np.eye(getnum(SW))
Fy(:,Sbus) = 0
Gx(Sbus,:) = 0
Fy(:,Gbus) = 0
Gx(Gbus,:) = 0
