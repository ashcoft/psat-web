# Module: psat.packages.phclassclass.warn
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def warn(a, idx, msg):

global Bus

fm_print(fm_strjoin('Warning: PHS #',int2str(idx),' between buses <', ...
	       Bus.names{a.bus1(idx)},'> and <', ...
               Bus.names{a.bus2(idx)},'> ',msg))