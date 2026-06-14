# Module: psat.packages.pqclassclass.findpos
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = findpos(a)

global CPF

idx = []
if not a.n, return, end

if CPF.onlypqgen
  idx = find(a.u & a.gen)
  if isempty(idx)
    fm_print('No PQ generator found. Expect meaningless results.')
elseif CPF.onlynegload
  idx = find(a.u.*a.con(:,4) < 0)
  if isempty(idx)
    fm_print('No negative load found. Expect meaningless results.')
elseif CPF.negload
  idx = find(a.u)
else
  idx = find(a.u.*a.con(:,4) >= 0)
