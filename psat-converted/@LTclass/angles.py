# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LTclass\angles.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [s12,c12] = angles(a)

global DAE

t1 = DAE.y(a.bus1)
t2 = DAE.y(a.bus2)

s12 = sin(t1-t2)
c12 = cos(t1-t2)
