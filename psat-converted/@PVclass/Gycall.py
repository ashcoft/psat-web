# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\Gycall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Gycall(p):

global Settings

if not p.n, return, end

if Settings.pv2pq
  fm_setgy(p.vbus(find(not p.pq & p.u)))
else
  fm_setgy(p.vbus(find(p.u)))
