# Module: psat.packages.pvclassclass.resetqlim
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = resetqlim(p)

global Settings

if not p.n, return, end

p.con(:,6) = p.store(:,6).*p.con(:,2)/Settings.mva
p.con(:,7) = p.store(:,7).*p.con(:,2)/Settings.mva