# Module: psat.packages.dmclassclass.tiebreaks
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function KTBD = tiebreaks(a)

global OPF

if not OPF.tiebreak,
  KTBD = np.zeros((a.n,1))
else
# Demand Tiebreaks
  if len(a.con(1,:)) < 15,
    KTBD = np.zeros((a.n,1))
  else,
    KTBD = a.u.*a.con(:,15)
  idx = find(a.u.*a.con(:,5) == 0)
  if not isempty(idx)
    KTBD(idx) = 0
  idx = find(a.u.*a.con(:,5))
  if not isempty(idx)
    KTBD(idx) = KTBD(idx)./a.con(idx,5)