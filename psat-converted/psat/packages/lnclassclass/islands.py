# Module: psat.packages.lnclassclass.islands
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def islands(a):

if not a.n, return, end

global Bus Ltc Phs Hvdc Lines

# looking for islanded buses
traceY = abs(sum(a.Y).'-diag(a.Y));
traceY = gettrace(Ltc,traceY)
traceY = gettrace(Phs,traceY)
traceY = gettrace(Hvdc,traceY)
traceY = gettrace(Lines,traceY)

Bus = islands(Bus,traceY)