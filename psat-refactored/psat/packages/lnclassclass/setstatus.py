# Module: psat.packages.lnclassclass.setstatus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setstatus(a,idx,u)

if not a.n, return, end
if isempty(idx), return, end

a.u(idx) = u
a = build_y(a)
islands(a)