# Module: psat.packages.hvclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.dat(idx,:) = []
a.bus1(idx) = []
a.bus2(idx) = []
a.v1(idx) = []
a.v2(idx) = []
a.n = a.n - len(idx)
a.Idc(idx) = []
a.xr(idx) = []
a.xi(idx) = []
a.cosa(idx) = []
a.cos(idx)g = []
a.phir(idx) = []
a.phii(idx) = []
a.Vrdc(idx) = []
a.Vidc(idx) = []
a.yr(idx) = []
a.yi(idx) = []
a.u(idx) = []