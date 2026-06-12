# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FLclass\setx0.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global DAE PQ Bus

if not a.n, return, end

V = DAE.y(a.vbus)

for i in range(1, a.n+1):
  idx = findbus(PQ,a.bus(i))
  if isempty(idx)
    fm_print(['No PQ load found for initializing frequency ', ...
             'dependent load at bus ',Bus.names{a.bus(i)}])
  else
    P = a.u(i)*PQ.P0(idx)*a.con(i,2)/100
    Q = a.u(i)*PQ.Q0(idx)*a.con(i,5)/100
    PQ = pqsub(PQ,idx,P,Q)
    a.con(i,2) = a.con(i,2)*PQ.P0(idx)/(V(i)^a.con(i,3))/100
    a.con(i,5) = a.con(i,5)*PQ.Q0(idx)/(V(i)^a.con(i,6))/100
    PQ = remove(PQ,idx,'zero')
DAE.x(a.x) = 0
DAE.y(a.dw) = 0
a.a0 = DAE.y(a.bus)

#check limits
fm_print('Initialization of Frequency Dependent Loads completed.')
