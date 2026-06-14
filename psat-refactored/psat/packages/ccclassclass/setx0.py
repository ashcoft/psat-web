# Module: psat.packages.ccclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global DAE

if not a.n, return, end

# variable initialization
DAE.x(a.q1) = 1
DAE.y(a.q) = 1

# pilot bus voltage reference
a.con(:,5) = DAE.y(a.vbus)

fm_print('Initialization of Central Area Controllers completed.')
