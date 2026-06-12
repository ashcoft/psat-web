# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@IMclass\xfirst.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def xfirst(a):

if not a.n, return, end

global DAE

DAE.x(a.slip) = not a.z.*a.u; #  slip = 1 at start-up

ord3 = find(a.con(:,5) == 3)
ord5 = find(a.con(:,5) == 5)

if not isempty(ord3)
  u = a.z(ord3).*a.u(ord3)
  DAE.x(a.e1r(ord3)) = 0.05*u
  DAE.x(a.e1m(ord3)) = 0.9*u

if not isempty(ord5)
  u = a.z(ord5).*a.u(ord5)
  DAE.x(a.e1r(ord5)) = 0.05*u
  DAE.x(a.e1m(ord5)) = 0.9*u
  DAE.x(a.e2r(ord5)) = 0.05*u
  DAE.x(a.e2m(ord5)) = 0.9*u
