# Module: psat.packages.ltclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Bus Settings

if not p.n, return, end

V1 = getkv(Bus,p.bus1,1)
V2 = getkv(Bus,p.bus2,1)

VL1 = p.con(:,4)
VL2 = VL1./p.con(:,6)

fm_errv(VL1,'Under Load Tap Changer',p.bus1)
fm_errv(VL2,'Under Load Tap Changer',p.bus2)

Vb2new = V1.*V1
Vb2old = VL1.*VL1

p.con(:,13)  = Settings.mva*Vb2old.*p.con(:,13)./p.con(:,3)./Vb2new
p.con(:,14)  = Settings.mva*Vb2old.*p.con(:,14)./p.con(:,3)./Vb2new

# reference voltage
idx = find(p.con(:,16) == 1 | p.con(:,16) == 3)
if not isempty(idx)
  p.con(idx,12) = p.con(idx,12)./V2(idx).*VL2(idx)

# reference reactive power
idx = find(p.con(:,16) == 2)
if not isempty(idx)
  p.con(idx,12) = Settings.mva*p.con(idx,12)./p.con(idx,3)