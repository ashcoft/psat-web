# Module: psat.packages.pqclassclass.Glcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Glcall(p):

global DAE

if not p.n, return, end

DAE.Gl(p.bus) = DAE.Gl(p.bus) + p.u.*p.con(:,4)
DAE.Gl(p.vbus) = DAE.Gl(p.vbus) + p.u.*p.con(:,5)