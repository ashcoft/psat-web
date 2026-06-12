# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\noshunt.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = noshunt(a)

if not a.n, return, end

idx = find(a.shunt)
if isempty(idx), return, end

global Bus

a.con(idx,7) = a.store(idx,7).*a.con(idx,3)./getkv(Bus,a.bus(idx),1)
a.con(idx,8) = a.store(idx,8)
a.shunt = np.zeros((a.n,1))
