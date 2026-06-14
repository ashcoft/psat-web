# Module: psat.packages.tpclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

global Settings

if not a.n, return, end

a.con(:,9) = a.con(:,9)./a.con(:,2)*Settings.mva
a.con(:,10) = a.con(:,10)./a.con(:,2)*Settings.mva
