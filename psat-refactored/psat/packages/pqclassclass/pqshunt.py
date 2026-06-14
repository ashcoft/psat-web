# Module: psat.packages.pqclassclass.pqshunt
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = pqshunt(p)

global DAE Settings

if not p.n, return, end

if not Settings.pq2z  or  Settings.init > 1, return, end

if Settings.forcepq
  fm_print(' * The option "Settings.forcepq" overwrites the option "Settings.pq2z".')
  fm_print(' * All PQ loads will be forced to consume constant powers.')
  return

p.shunt = not p.gen
idx = find(p.shunt)
if isempty(idx), return, end
p.con(idx,7) = DAE.y(p.vbus(idx))
p.con(idx,8) = 0