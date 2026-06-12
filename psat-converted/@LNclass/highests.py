# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\highests.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function values = highests(a)

global DAE Bus Settings Varname Varout

values = []

if not a.n, return, end

n1 = DAE.n+DAE.m+2*Bus.n+6*Settings.nseries
idx = find(Varname.idx > n1 & Varname.idx <= n1+a.n)

if isempty(idx), return, end

out = Varout.vars(:,idx)

for k in range(1, len(idx)+1):
  h = Varname.idx(idx(k)) - n1
  if a.con(h,15)
    out(:,k) = out(:,k)/a.con(h,15)

vals = max(out,[],1)
[y,jdx] = sort(vals,2,'descend')

if len(jdx) > 3, jdx = jdx(1:3); end

values = idx(jdx)
