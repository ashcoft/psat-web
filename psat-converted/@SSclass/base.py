# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SSclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Line Bus

if not p.n, return, end

fm_errv(p.con(:,4),'Sssc',p.bus1)
Vb = getkv(Bus,p.bus1,1)
p.con(:,9)  = p.con(:,9).*p.con(:,4)./Vb
p.con(:,10) = p.con(:,10).*p.con(:,4)./Vb

[p.xcs,p.y] = factsbase(Line,p.line,p.Cp,'SSSC')
