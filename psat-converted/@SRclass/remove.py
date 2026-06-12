# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SRclass\remove.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.bus(idx) = []
a.vbus(idx) = []
a.n = a.n - len(idx)
a.Id(idx) = []
a.Iq(idx) = []
a.If(idx) = []
a.Edc(idx) = []
a.Eqc(idx) = []
a.Tm(idx) = []
a.Efd(idx) = []
a.delta_HP(idx) = []
a.omega_HP(idx) = []
a.delta_IP(idx) = []
a.omega_IP(idx) = []
a.delta_LP(idx) = []
a.omega_LP(idx) = []
a.delta(idx) = []
a.omega(idx) = []
a.delta_EX(idx) = []
a.omega_EX(idx) = []
a.u(idx) = []
