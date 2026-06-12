# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\swsum.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def swsum(a, k):

global SW

if not a.n, return, end

for i in range(1, a.n+1):
  idx = findbus(SW,a.bus(i))
  SW = swsum(SW,idx,k*a.con(i,6)*a.u(i))
        
