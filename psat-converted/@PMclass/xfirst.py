# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PMclass\xfirst.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def xfirst(a):

global DAE

if not a.n, return, end

DAE.x(a.vm) = np.ones((a.n,1))
DAE.x(a.thetam) = np.zeros((a.n,1))
