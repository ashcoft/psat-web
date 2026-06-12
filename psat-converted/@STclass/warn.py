# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@STclass\warn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def warn(a, idx, msg):

global Bus

fm_print(fm_strjoin('Warning: STATCOM #',int2str(idx),' at bus <', ...
               Bus.names(a.bus(idx)),'>: ',msg))