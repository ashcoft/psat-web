# Module: psat.packages.dmclassclass.pdbound
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function pd = pdbound(a,pd)

pd = max(pd,a.u.*a.con(:,6))
pd = min(pd,a.u.*a.con(:,5))