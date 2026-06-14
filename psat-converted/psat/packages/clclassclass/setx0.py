# Module: psat.packages.clclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global DAE

if not a.n, return, end

# variable initialization
DAE.x(a.Vs) = 0
Vs = DAE.x(a.Vs)

# check time constants
idx = find(a.con(:,4) == 0)
if idx
  warn(a,idx,'Time constant T cannot be zero. T = 0.001 s will be used.')
a.con(idx,4) = 0.001

# Reactive power reference
a.con(:,7) = DAE.y(a.q)

a.dVsdQ = (a.con(:,5)+a.con(:,6))./a.con(:,4)
#a.u = ones(a.n,1);

# check limits
idx = find(Vs > a.con(:,8))
if idx
  warn(a,idx,' State variable Vs is over its maximum limit.')
idx = find(Vs < a.con(:,9))
if idx
  warn(a,idx,' State variable Vs is under its minimum limit.')

fm_print('Initialization of Cluster Controllers completed.')
  