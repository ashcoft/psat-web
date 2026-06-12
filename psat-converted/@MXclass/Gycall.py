# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@MXclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def Gycall(a):

global DAE Settings

if not a.n, return, end

V1 = DAE.y(a.vbus)
Kpf = a.con(:,5)
Kpv = a.con(:,6)
alpha = a.con(:,7)
Tpv = a.con(:,8)
Kqf = a.con(:,9)
Kqv = a.con(:,10)
beta = a.con(:,11)
Tqv = a.con(:,12)
Tfv = a.con(:,13)
Tft = a.con(:,14)
k = 0.5/np.pi/Settings.freq
V0 = a.dat(:,1)

DAE.Gy = DAE.Gy + sparse(a.bus,a.vbus,a.u.*Kpv.*((V1./V0).^alpha.*alpha./V1+Tpv./Tfv),DAE.m,DAE.m)
DAE.Gy = DAE.Gy + sparse(a.bus,a.bus,a.u.*Kpf.*k./Tft,DAE.m,DAE.m)
DAE.Gy = DAE.Gy + sparse(a.vbus,a.vbus,a.u.*Kqv.*((V1./V0).^beta.*beta./V1+Tqv./Tfv),DAE.m,DAE.m)
DAE.Gy = DAE.Gy + sparse(a.vbus,a.bus,a.u.*Kqf.*k./Tft,DAE.m,DAE.m)
