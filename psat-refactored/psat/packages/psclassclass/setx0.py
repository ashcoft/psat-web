# Module: psat.packages.psclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setx0(a)

global DAE

if not a.n, return, end

type = a.con(:,2)
ty1 = find(type == 1)
tya = find(type > 1)
tyb = find(type > 3)

VSI = np.zeros((a.n,1))
SIw = find(a.con(:,3) == 1)
SIp = find(a.con(:,3) == 2)
SIv = find(a.con(:,3) == 3)
if SIw, VSI = DAE.x(a.omega(SIw)); end
if SIp, VSI = DAE.y(a.p(SIp)); end
if SIv, VSI = DAE.y(a.vbus(SIv)); end

SIp = find(a.con(:,3) == 2 & type > 1)
SIv = find(a.con(:,3) == 3 & type > 1)

a.con(SIp,14) = a.con(SIp,6)
a.con(find(a.con(:,3) != 2 & type > 1),14) = 0
a.con(SIp,6) = 0
a.con(SIv,15) = a.con(SIv,6)
a.con(find(a.con(:,3) != 3 & type > 1),15) = 0
a.con(SIv,6) = 0

Kw = a.u.*a.con(:,6)
Kp = a.u.*a.con(:,14)
Kv = a.u.*a.con(:,15)

Tw = a.con(:,7)
T2 = a.con(:,9)
T4 = a.con(:,11)
Ta = a.con(:,13)

idx = find(Tw == 0)
if idx,
  a.con(idx,6) = 0.01
  warn(a,idx,[' Tw cannot be zero. Default value Tw = 0.01 will' ...
              ' be used.'])
if ty1
  DAE.x(a.v1(ty1)) = -Kw(ty1)-Kp(ty1).*DAE.y(a.p(ty1)) ...
      -Kv(ty1).*DAE.y(a.vbus(ty1))
if tya
  idx = find(T2(tya) == 0)
  if idx,
    a.con(tya(idx),9) = 0.01
    warn(a,idx,[' T2 cannot be zero. Default value T2 = 0.01 will' ...
                ' be used.'])
  idx = find(T4(tya) == 0)
  if idx,
    a.con(tya(idx),11) = 0.01
    warn(a,idx,[' T4 cannot be zero. Default value T4 = 0.01 will' ...
                ' be used.'])
  DAE.x(a.v1(tya)) = -(Kw(tya)+Kp(tya)+Kv(tya)).*VSI(tya)
  DAE.x(a.v2(tya)) = 0
  DAE.x(a.v3(tya)) = 0
if tyb
  idx = find(Ta(tyb) == 0)
  if idx,
    a.con(tyb(idx),13) = 0.01
    warn(a,idx,[' Ta cannot be zero. Default value Ta = 0.01 will' ...
                ' be used.'])
  DAE.x(a.va(tyb)) = 0

idx = find(a.con(:,22) == 0)
a.con(:,22) = 0
if not isempty(idx)
  a.con(idx,22) = -1

DAE.y(a.vss) = 0

fm_print('Initialization of Power System Stabilizers completed.')