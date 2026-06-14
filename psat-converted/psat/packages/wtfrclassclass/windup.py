# Module: psat.packages.wtfrclassclass.windup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def windup(p):

csi_max = p.con(:, 10)
csi_min = p.con(:, 11)

fm_windup(p.csi, csi_max, csi_min, 'td')