# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\findantennas.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [busidx,lineidx] = findantennas(a)
# FINDANTENNAS finds buses in antenna and returns the indexes
#              of buses and of the unique connected lines
#
# BUSIDX:  indexes of buses in antenna
# LINEIDX: indexes of lines connected to buses in antenna
#
global Bus

busidx = 0
lineidx = []

if not a.n, return, end

nl = [1:a.n]
ivec = sparse(nl,a.fr,1,a.n,Bus.n)
jvec = sparse(nl,a.to,1,a.n,Bus.n)
lineidx = find(sum([ivec;jvec],1)==1)

print(' ')

if isempty(lineidx)
  busidx = 0
  fm_print('All lines are used for (N-1) contingency evaluations.')
else
  busidx = find(sum(ivec(lineidx,:)+jvec(lineidx,:),2))
  fm_print('Detected the following antennas:')
  fm_print(fm_strjoin('Bus "',Bus.names(busidx),'" is in antenna.'))
  fm_print(['When these lines are out, connected generators ', ...
           'and/or loads will be neglected.'])
