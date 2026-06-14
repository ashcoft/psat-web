# Module: psat.packages.buclassclass.gisland
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def gisland(a):

global DAE

if isempty(a.island), return, end

kkk = a.island
jjj = kkk+a.n

DAE.g(kkk) = 0
DAE.g(jjj) = 0

DAE.y(kkk) = 0
DAE.y(jjj) = 1e-6