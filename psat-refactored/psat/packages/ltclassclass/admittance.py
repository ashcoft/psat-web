# Module: psat.packages.ltclassclass.admittance
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function y = admittance(a)

global DAE

x = a.con(:,13)
r = a.con(:,14)
z = r+i*x
y = 1./z