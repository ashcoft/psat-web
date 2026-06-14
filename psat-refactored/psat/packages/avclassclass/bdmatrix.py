# Module: psat.packages.avclassclass.bdmatrix
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def bdmatrix(a):

global LA DAE

LA.b_avr = []
LA.d_avr = []

if not a.n
  fm_print('* * * No automatic voltage control found')
  return

Fu = sparse(DAE.n,a.n)
Gu = sparse(a.vref,1:a.n,a.u,DAE.m,a.n)

# B & D matrix for Vref0
LA.d_avr = -full(DAE.Gy\Gu)
LA.b_avr = full(Fu + DAE.Fy*LA.d_avr)