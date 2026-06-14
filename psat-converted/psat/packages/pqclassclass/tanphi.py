# Module: psat.packages.pqclassclass.tanphi
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function val = tanphi(a,idx)

val = []
if not a.n, return, end

if isnumeric(idx)
  p = a.con(idx,4)
  jdx = find(p == 0)
  if not isempty(jdx), p(jdx) = 0; end
  val = a.u(idx).*a.con(idx,5)./p
  if not isempty(jdx), val(jdx) = 1; end
elseif strcmp(idx,'all')
  p = a.con(:,4)
  jdx = find(p == 0)
  if not isempty(jdx), p(jdx) = 1; end
  val = a.u.*a.con(:,5)./p
  if not isempty(jdx), val(jdx) = 0; end