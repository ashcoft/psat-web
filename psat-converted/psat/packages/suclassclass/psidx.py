# Module: psat.packages.suclassclass.psidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = psidx(a,k)

global Bus

idx = sparse(a.bus,[1:a.n],k,Bus.n,a.n)
