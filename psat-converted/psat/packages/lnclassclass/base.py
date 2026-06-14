# Module: psat.packages.lnclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function p = base(p)

global Bus Settings

if not p.n, return, end

# look for transformers (kt != 0)
idx = find(p.con(:,7))
kt = p.con(idx,7)
VL1 = p.con(:,4)

# set zero length for transformers
p.con(idx,6) = np.zeros((len(idx),1))
V1 = getkv(Bus,p.fr,1)
V2 = getkv(Bus,p.to,1)
KT = V1(idx)./V2(idx)

# check consistency of voltage bases
if not isempty(kt)
  corr = abs(kt-KT)./KT
  idx1 = find(corr > 0.1)
for i in range(1, len(idx1)+1):
    k1 = Bus.names{p.fr(idx(idx1(i)))}
    k2 = Bus.names{p.to(idx(idx1(i)))}
    fm_print(['Tap ratio of transformer #',num2str(idx(idx1(i))), ...
             ' from bus <', k1, '> to bus <', k2, ...
             '> differs more than 10% from the bases defined at', ...
             ' connected buses.'])
# adjust tap ratio if voltage bases do not match
  idx_m = find(p.con(idx,11) == 0)
  p.con(idx(idx_m),11) = 1
  p.con(idx,11) = p.con(idx,11).*kt./KT
idx2 = find(abs(VL1-V1)./V1 > 0.1)
for i in range(1, len(idx2)+1):
  k1 = Bus.names{p.fr(idx2(i))}
  k2 = Bus.names{p.to(idx2(i))}
  fm_print(['Voltage of Line #',num2str(idx2(i)), ...
           ' from bus <', k1,'> to bus <', k2, ...
           '> differs more than 10% from the base defined at', ...
           ' the connected bus <', k1,'>'])

# Voltage rates
Vb2new = V1.*V1
Vb2old = VL1.*VL1

# report line parameters to system base [Sb]
p.con(:,8)  = Vb2old.*p.con(:,8)./p.con(:,3)./Vb2new*Settings.mva
p.con(:,9)  = Vb2old.*p.con(:,9)./p.con(:,3)./Vb2new*Settings.mva
p.con(:,10) = Vb2new.*p.con(:,10).*p.con(:,3)./Vb2old/Settings.mva

# report line limits to system bases
p.con(:,13) = p.con(:,13).*p.con(:,3).*V1./VL1/Settings.mva
p.con(:,14) = p.con(:,14).*p.con(:,3)/Settings.mva
p.con(:,15) = p.con(:,15).*p.con(:,3)/Settings.mva