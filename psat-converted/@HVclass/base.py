# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@HVclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

global Bus Settings

if not a.n, return, end

fm_errv(a.con(:,4),'Hvdc',a.bus1)
fm_errv(a.con(:,5),'Hvdc',a.bus2)

Vb2old = a.con(:,4).*a.con(:,4)
Vb2new = getkv(Bus,a.bus1,2)

k = Settings.mva*Vb2old./a.con(:,3)./Vb2new
a.con(:,9) = k.*a.con(:,9)

Vb2old = a.con(:,5).*a.con(:,5)
Vb2new = getkv(Bus,a.bus2,2)

k = Settings.mva*Vb2old./a.con(:,3)./Vb2new
a.con(:,10) = k.*a.con(:,10)
