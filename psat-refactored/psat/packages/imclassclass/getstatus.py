# Module: psat.packages.imclassclass.getstatus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function u = getstatus(a)

global DAE

u = (a.con(:,18) <= DAE.t | a.z) & a.u