# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\filter.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [idx1,idx2,busidx1,busidx2] = filter(a,buslist)
# filter lines using bus list

idx1 = cell(0,0)
idx2 = cell(0,0)
busidx1 = []
busidx2 = []

fr = a.fr.*a.u
to = a.to.*a.u

for i in range(1, len(buslist)+1):
  
  idxfr = find(fr == buslist(i))
  idxto = find(to == buslist(i))

  if not isempty(idxfr)
    idx = []
for h in range(1, len(idxfr)+1):
      k = idxfr(h)
      jdx = find(buslist == to(k))
      if isempty(jdx), idx = [idx; k]; end
    if not isempty(idx)
      idx1{end+1,1} = idx
      busidx1 = [busidx1; i]
  
  if not isempty(idxto)
    idx = []
for h in range(1, len(idxto)+1):
      k = idxto(h)
      jdx = find(buslist == fr(k))
      if isempty(jdx), idx = [idx; k]; end
    if not isempty(idx)
      idx2{end+1,1} = idx
      busidx2 = [busidx2; i]


