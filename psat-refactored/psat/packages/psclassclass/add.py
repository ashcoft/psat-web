# Module: psat.packages.psclassclass.add
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = add(a,data)

global Bus Syn Exc

a.n = a.n + len(data(1,:))
a.con = [a.con; data]
a.exc = [a.exc; data(:,1)]
a.syn = Exc.syn(a.exc)
a.bus = getbus(Syn,a.syn)
a.vbus= a.bus + Bus.n
