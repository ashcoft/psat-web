# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Bus Settings

if not p.n, return, end

fm_errv(p.con(:,3),'Synchronous Machine',p.bus)
Vb2new = getkv(Bus,p.bus,2)
Vb2old = p.con(:,3).*p.con(:,3)
k = Settings.mva*Vb2old./p.con(:,2)./Vb2new
i = [6:10, 13:15]
for h in range(1, len(i)+1):
  p.con(:,i(h))= k.*p.con(:,i(h))
p.con(:,18) = p.con(:,18).*p.con(:,2)/Settings.mva
p.con(:,19) = p.con(:,19).*p.con(:,2)/Settings.mva
