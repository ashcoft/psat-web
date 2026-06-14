# Module: psat.packages.ltclassclass.angles
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [s12,c12] = angles(a)

global DAE

t1 = DAE.y(a.bus1)
t2 = DAE.y(a.bus2)

s12 = sin(t1-t2)
c12 = cos(t1-t2)