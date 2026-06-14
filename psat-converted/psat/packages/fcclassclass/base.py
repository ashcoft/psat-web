# Module: psat.packages.fcclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

global Bus Settings

if not a.n, return, end

Vn = a.con(:,3)
Vb2 = getkv(Bus,a.bus,2)

fm_errv(Vn,'Solid Oxide Fuel Cell',a.bus)

Vn2 = Vn.*Vn

a.con(:,26) = Vn2.*a.con(:,26)./a.con(:,2)./Vb2*Settings.mva