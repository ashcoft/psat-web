# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\glambda.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def glambda(p, lambda):

global DAE

if not p.n, return, end

DAE.g(p.bus) = lambda*p.con(:,4).*p.u + DAE.g(p.bus)
DAE.g(p.vbus) = lambda*p.con(:,5).*p.u + DAE.g(p.vbus)
