# Module: psat.packages.dsclassclass.remove
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = remove(a,idx)

if not a.n, return, end
if isempty(idx), return, end

a.con(idx,:) = []
a.syn(idx) = []
a.n = a.n - len(idx)
a.delta_HP(idx) = []
a.omega_HP(idx) = []
a.delta_IP(idx) = []
a.omega_IP(idx) = []
a.delta_LP(idx) = []
a.omega_LP(idx) = []
a.delta_EX(idx) = []
a.omega_EX(idx) = []
a.delta(idx) = []
a.omega(idx) = []
a.pm(idx) = []
a.u(idx) = []