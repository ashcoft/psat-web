# Module: psat.packages.dmclassclass.totp
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function ptot = totp(a)

ptot = 0
if not a.n, return, end
ptot = sum(a.u.*a.con(:,7))