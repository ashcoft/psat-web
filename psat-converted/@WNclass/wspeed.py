# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WNclass\wspeed.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function Vw = wspeed(a)

global DAE Settings

Vw = np.zeros((a.n,1))
t = DAE.t
if t < 0, t = Settings.t0; end

if t == Settings.t0
  Vw = a.vwa
else
for i in range(1, a.n+1):
    Vw(i) = interp1(a.speed(i).time,a.speed(i).vw,t)
