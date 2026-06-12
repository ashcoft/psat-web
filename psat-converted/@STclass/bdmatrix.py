# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@STclass\bdmatrix.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE 

LA.b_statcom = []
LA.d_statcom = []

if not a.n
  fm_print('* * * No Statcom device found')
  return

Fu = sparse(DAE.n,a.n)
Gu = sparse(a.vref,1:a.n,a.u,DAE.m,a.n)

# B & D matrix for reference voltage
LA.d_statcom = -full(DAE.Gy\Gu)
LA.b_statcom = full(Fu + DAE.Fy*LA.d_statcom)

