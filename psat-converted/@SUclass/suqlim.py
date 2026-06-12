# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\suqlim.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [qx,qn] = suqlim(a,Qmax,Qmin,bus)

if not a.n
  qx = []
  qn = []
  return

qx = np.zeros((a.n, 1))
qn = np.zeros((a.n, 1))

for i in range(1, len(bus)+1):
  idx = find(a.bus == bus(i))
  if isempty(idx), continue, end
  qx(idx) = a.u(idx).*a.con(idx,16)+1e-8*(not a.u(idx))
  qn(idx) = a.u(idx).*a.con(idx,17)
  maxq = sum(abs(a.u(idx).*a.con(idx,16)))
  minq = sum(abs(a.u(idx).*a.con(idx,17)))
  if maxq == 0
    qx(idx) = (Qmax(i)/len(idx))*a.u(idx)+1e-8*(not a.u(idx))
  if minq == 0
    qn(idx) = (Qmin(i)/len(idx))*a.u(idx)

