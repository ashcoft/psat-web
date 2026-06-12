# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@MNclass\setx0.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

if not a.n, return, end

global PQ DAE Bus

V = DAE.y(a.vbus)

i = find(a.con(:,8))
for j in range(1, len(i)+1):
  k = i(j)
  idx = findbus(PQ,a.bus(k))
  if isempty(idx),
    fm_print(['No PQ load found for initializing monomial ', ...
             'load at bus ',Bus.names{a.bus(k)}])
  else
    P = a.u(k)*PQ.P0(idx)*a.con(k,4)/100
    Q = a.u(k)*PQ.Q0(idx)*a.con(k,5)/100
    PQ = pqsub(PQ,idx,P,Q)
    a.con(k,4)  = a.con(k,4)*PQ.P0(idx)/(V(k)^a.con(k,6))/100
    a.con(k,5)  = a.con(k,5)*PQ.Q0(idx)/(V(k)^a.con(k,7))/100
    PQ = remove(PQ,idx,'zero')

fm_print('Initialization of Monomial Loads completed.')
