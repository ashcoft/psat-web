# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\warn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def warn(a, idx, msg):

global Bus

fm_print(fm_strjoin('Warning: Synchronous Machine #', ...
               int2str(idx),'(model ',num2str(a.con(idx,5)), ...
               ') at bus ',Bus.names(a.bus(idx)),msg))