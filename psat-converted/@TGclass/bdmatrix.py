# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\bdmatrix.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE 

LA.b_tg = []
LA.d_tg = []

if not a.n
  fm_print('* * * No turbine governor found')
  return

Fu = sparse(DAE.n,a.n)
Gu = sparse(a.wref,1:a.n,a.u,DAE.m,a.n)

# B & D matrix for reference speed
LA.d_tg = -full(DAE.Gy\Gu)
LA.b_tg = full(Fu + DAE.Fy*LA.d_tg)
