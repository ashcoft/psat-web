# Module: psat.packages.vlclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Settings

if not p.n, return, end

p.con(:,6) = p.con(:,6).*p.con(:,2)/Settings.mva
p.con(:,7) = p.con(:,7).*p.con(:,2)/Settings.mva
p.con(:,8) = p.con(:,8).*p.con(:,2)/Settings.mva
p.con(:,9) = p.con(:,9).*p.con(:,2)/Settings.mva