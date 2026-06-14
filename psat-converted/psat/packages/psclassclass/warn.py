# Module: psat.packages.psclassclass.warn
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def warn(a, idx, msg):

global Bus

fm_print(fm_strjoin('Warning: PSS #',int2str(idx),' at bus #', ...
               Bus.names{a.bus(idx)},msg))