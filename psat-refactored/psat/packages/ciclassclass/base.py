# Module: psat.packages.ciclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

global Syn

if not a.n, return, end

# reset generator parameters
a.M = getvar(Syn,a.gen,'M')
for i in range(1, a.n+1):
  idx = a.syn{i}
  a.Mtot(i,1) = sum(a.M(idx))

