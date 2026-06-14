# Module: psat.packages.suclassclass.psupper
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = psupper(a,ps)

idx = find(ps > a.u.*a.con(:,4))