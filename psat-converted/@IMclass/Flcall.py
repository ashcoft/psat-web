# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@IMclass\Flcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Flcall(a):

global DAE

if not a.n, return, end

slip = DAE.x(a.slip)
u = getstatus(a)
A = a.dat(:,1)
B = a.dat(:,2)
C = a.dat(:,3)
i2Hm = u.*a.dat(:,4)
Tm = A + slip.*(B + slip.*C)

# check if the motor can work as a brake
z = slip < 1 | a.con(:,19) | DAE.f(a.slip) != 0

DAE.Fl = DAE.Fl + sparse(a.slip,1,z.*Tm.*i2Hm,DAE.n,1)
