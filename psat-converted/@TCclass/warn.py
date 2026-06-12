# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TCclass\warn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def warn(a, idx, msg):

fm_print(fm_strjoin('Warning: TCSC #',int2str(idx),' between buses #', ...
	       int2str(a.bus1(idx)),' and #',int2str(a.bus2(idx)),msg))