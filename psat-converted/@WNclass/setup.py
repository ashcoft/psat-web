# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WNclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setup(a)

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
for i in range(1, a.n+1):
  a.speed(i).time = []
a.store = a.con
