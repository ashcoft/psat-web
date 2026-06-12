# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WTFRclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.gen(idx) = []
a.freq(idx) = []
a.dat(idx,:) = []
a.n = a.n - len(idx)
a.u(idx) = []
a.we(idx) = []
a.Df(idx) = []
a.Dfm(idx) = []
a.x(idx) = []
a.csi(idx) = []
a.pfw(idx) = []
a.pwa(idx) = []
a.pf1(idx) = []
a.pout(idx) = []
