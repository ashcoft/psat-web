# Module: psat.packages.dsclassclass.add
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = add(a,data)

a.n = a.n + len(data(1,:))
a.con = [a.con; data]
a.syn = [a.syn; round(data(:,1))]