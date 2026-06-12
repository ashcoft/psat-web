# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\findpos.m  (upstream PSAT, GPL-2.0+)
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

