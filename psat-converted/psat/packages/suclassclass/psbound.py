# Module: psat.packages.suclassclass.psbound
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function ps = psbound(a,ps)

ps = max(ps,a.u.*a.con(:,5))
ps = min(ps,a.u.*a.con(:,4))