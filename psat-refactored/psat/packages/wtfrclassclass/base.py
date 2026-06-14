# Module: psat.packages.wtfrclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)

global Settings Dfig

if not p.n, return, end

Sn = Dfig.con(p.gen, 3)

p.con(:, 13) = p.con(:, 13).*Sn/Settings.mva
p.con(:, 14) = p.con(:, 14).*Sn/Settings.mva