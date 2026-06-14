# Module: psat.packages.phclassclass.admittance
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function y = admittance(a)

r = a.con(:,11)
x = a.con(:,12)
z = r+i*x
y = 1./z