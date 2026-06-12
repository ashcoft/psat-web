# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\write.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def write(a, fid, buslist):

# write transmission line and transformer data

# filter lines using bus list
idx = []
for i in range(1, a.n+1):
  idxfr = find(buslist == a.fr(i)*a.u(i))
  idxto = find(buslist == a.to(i)*a.u(i))
  if not isempty(idxfr)  and  not isempty(idxto), idx = [idx; i]; end

if isempty(idx), return, end

# write line data
fprintf(fid,'Line.con = [ Line.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],a.con(idx,:)');
fprintf(fid,'   ];\n\n')

