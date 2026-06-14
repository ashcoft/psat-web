# Module: psat.packages.suclassclass.tiebreaks
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function KTBS = tiebreaks(a)

global OPF

if not OPF.tiebreak,
  KTBS = np.zeros((a.n,1))
else
# a Tiebreaks
  if len(a.con(1,:)) < 14
    KTBS = np.zeros((a.n,1))
  else
    KTBS = a.u.*a.con(:,14)
  idx = find(a.u.*a.con(:,4) == 0)
  if not isempty(idx)
    KTBS(idx) = 0
  idx = find(a.u.*a.con(:,4))
  if not isempty(idx)
    KTBS(idx) = KTBS(idx)./a.con(idx,4)