# Module: psat.packages.mnclassclass.write
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def write(a, fid, buslist):

# write voltage dependent loads loads

if not a.n, return, end

# filter loads using bus list
idx = []
for i in range(1, a.n+1):
  jdx = find(buslist == a.bus(i)*a.u(i))
  if not isempty(jdx), idx = [idx; i]; end

if isempty(idx), return, end

# write Mn data
fprintf(fid,'Mn.con = [ Mn.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],a.con(idx,:)');
fprintf(fid,'   ];\n\n')