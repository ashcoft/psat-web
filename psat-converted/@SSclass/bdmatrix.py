# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SSclass\bdmatrix.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE 

LA.b_sssc = []
LA.d_sssc = []

if not a.n
  fm_print('* * * No SSSC device found')
  return


ty3 = find(a.con(:,2) == 3);  #  Constant P control

iv = 1:2:2*a.n;   #  index of V0 for any operation mode (V,X, or P constant)
ip = 2:2:2*a.n;   #  index of Pref for P constant operation mode

Fu = sparse(DAE.n,2*a.n)
Gu = sparse(a.v0,iv,a.u,DAE.m,2*a.n) + ...
     sparse(a.pref(ty3),ip(ty3),a.u(ty3),DAE.m,2*a.n)

# B & D matrix for SSSC references
LA.d_sssc = -full(DAE.Gy\Gu)
LA.b_sssc = full(Fu + DAE.Fy*LA.d_sssc)