# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PLclass\write.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def write(a, fid, buslist):

# write polynomial loads

if not a.n, return, end

# filter loads using bus list
idx = []
for i in range(1, a.n+1):
  jdx = find(buslist == a.bus(i)*a.u(i))
  if not isempty(jdx), idx = [idx; i]; end

if isempty(idx), return, end

# write Pl data
fprintf(fid,'Pl.con = [ Pl.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],a.con(idx,:)');
fprintf(fid,'   ];\n\n')
