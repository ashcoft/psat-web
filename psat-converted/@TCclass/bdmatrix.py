# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\bdmatrix.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE 

LA.b_tcsc = []
LA.d_tcsc = []

if not a.n
  fm_print('* * * No TCSC device found')
  return

ty2 = find(a.con(:,3) == 2);  #  Constant P control

ix = 1:2:2*a.n;   #  index of X0 for any operation mode (X or P constant)
ip = 2:2:2*a.n;   #  index of Pref for P constant operation mode
# ix = find(a.con(:,3) == 1); % index - operation mode x constant
# ip = find(a.con(:,3) == 2); % index - operation mode P constant

Fu = sparse(DAE.n,2*a.n)
Gu = sparse(a.x0,ix,a.u,DAE.m,2*a.n) + ...
    sparse(a.pref(ty2),ip(ty2),a.u(ty2),DAE.m,2*a.n)

# B & D matrix for TCSC references
LA.d_tcsc = -full(DAE.Gy\Gu)
LA.b_tcsc = full(Fu + DAE.Fy*LA.d_tcsc)
