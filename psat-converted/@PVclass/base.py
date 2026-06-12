# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Bus Settings

if not p.n, return, end

fm_errv(p.con(:,3),'PV Bus',p.bus)
Vb = getkv(Bus,p.bus,1)
p.con(:,4) = p.con(:,4).*p.con(:,2)/Settings.mva
p.con(:,6) = p.con(:,6).*p.con(:,2)/Settings.mva
p.con(:,7) = p.con(:,7).*p.con(:,2)/Settings.mva
p.con(:,8) = p.con(:,8).*p.con(:,3)./Vb
p.con(:,9) = p.con(:,9).*p.con(:,3)./Vb
