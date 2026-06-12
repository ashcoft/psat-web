# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PHclass\angles.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [s12a,c12a] = angles(a)

global DAE

alpha  = DAE.x(a.alpha)
t1 = DAE.y(a.bus1)
t2 = DAE.y(a.bus2)

s12a = sin(t1-t2-alpha)
c12a = cos(t1-t2-alpha)
