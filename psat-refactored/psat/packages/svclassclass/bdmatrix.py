# Module: psat.packages.svclassclass.bdmatrix
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE 

LA.b_svc = []
LA.d_svc = []

if not a.n
  fm_print('* * * No SVC device found')
  return

Fu = sparse(DAE.n,a.n)
Gu = sparse(a.vref,1:a.n,a.u,DAE.m,a.n)

# B & D matrix for reference voltage
LA.d_svc = -full(DAE.Gy\Gu)
LA.b_svc = full(Fu + DAE.Fy*LA.d_svc)
