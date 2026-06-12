# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/tests\d_motor_mdl.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
Bus.con = [ ... 
  1  132  1  0  1  1
  2  132  1  0  1  1
 ]

Line.con = [ ... 
  2  1  100  132  60  0  0  0.01  0.1  0.001  0  0  0  0  0  1
 ]

SW.con = [ ... 
  2  100  132  1.05  0  1.5  -1.5  1.1  0.9  0.8  1  1  1
 ]

Ind.con = [ ... 
  1  100  132  60  1  1  0.01  0.15  0.05  0.15  0.001  0.04  5  3  0.5  0  0  0  0  1
  1  100  132  60  3  1  0.01  0.15  0.05  0.15  0.001  0.04  5  3  0.25  0  0  1  0  1
  1  100  132  60  5  0  0.01  0.15  0.05  0.15  0.001  0.04  5  3  0.13  0.02  0.024  1  0  1
 ]

Bus.names = {... 
  'Bus1'; 'Bus2'}

