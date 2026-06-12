# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\growth.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function data = growth(a,rr,idx)

data = []

if not a.n, return, end

data = [a.con(:,[1 2]),a.con(:,4).*rr(idx(a.bus)),a.con(:,5).*rr(idx(a.bus)),np.zeros((a.n,13),np.ones((a.n,1)])
