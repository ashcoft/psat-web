# Module: psat.packages.pvclassclass.Gycall
# Refactored from psat-converted
# ------------------------------------------------------------------
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