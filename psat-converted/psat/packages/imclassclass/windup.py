# Module: psat.packages.imclassclass.windup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def windup(a):

idx = find(not a.con(:,19))
if not isempty(idx)
  fm_windup(a.slip(idx),1,-1e3,'td')