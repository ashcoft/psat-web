# Module: psat.packages.pmclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global DAE

if not a.n, return, end

DAE.x(a.vm) = a.u.*DAE.y(a.vbus)
DAE.x(a.thetam) = a.u.*DAE.y(a.bus)

idx = find(a.con(:,4) == 0)
if not isempty(idx)
  warn(a,idx, [' Time constant Tv cannot be 0. Tv = 0.05 will be ' ...
               'used.'])
  a.con(idx,4) = 0.05

idx = find(a.con(:,5) == 0)
if not isempty(idx)
  warn(a,idx, ' Time constant Ta cannot be 0. Ta = 0.05 will be used.')
  a.con(idx,5) = 0.05

a.dat = [1./a.con(:,4), 1./a.con(:,5)]

fm_print('Initialization of PMUs completed.')

