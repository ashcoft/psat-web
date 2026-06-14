# Module: psat.packages.phclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gcall(a):

global DAE

if not a.n, return, end

Vf = a.u.*DAE.y(a.v1).*exp(i*DAE.y(a.bus1))
Vt = a.u.*DAE.y(a.v2).*exp(i*DAE.y(a.bus2))
y = admittance(a)
m = a.con(:,15).*exp(i*DAE.x(a.alpha))

Ss = Vf.*conj((Vf./m-Vt).*y./conj(m))
Sr = Vt.*conj((Vt-Vf./m).*y)

DAE.g = DAE.g + ...
        sparse(a.bus1,1,real(Ss),DAE.m,1) + ...
        sparse(a.bus2,1,real(Sr),DAE.m,1) + ...
        sparse(a.v1,1,imag(Ss),DAE.m,1) + ...
        sparse(a.v2,1,imag(Sr),DAE.m,1)