# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BFclass\setx0.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setx0(a)

global DAE Settings

if not a.n, return, end

x = DAE.x(a.x)
w = DAE.x(a.w)
theta = DAE.y(a.bus)
Tf = a.con(:,2)
Tw = a.con(:,3)
theta0 = a.dat(:,1)
k = a.dat(:,2)

#check time constants
idx = find(Tf == 0)
if idx
  warn(a,idx, ['Time constant Tf cannot be zero. Tf = 0.001 ' ...
               's will be used.'])
a.con(idx,2) = 0.001
idx = find(Tw == 0)
if idx
  warn(a,idx, ['Time constant Tw cannot be zero. Tw = 0.001 ' ...
               's will be used.'])
a.con(idx,3) = 0.001

#variable initialization
DAE.x(a.x) = 0
DAE.x(a.w) = a.u
a.dat(:,1) = theta
a.dat(:,2) = 1./Tf/(2*np.pi*Settings.freq)

fm_print('Initialization of Bus Frequency Measurement completed.')

