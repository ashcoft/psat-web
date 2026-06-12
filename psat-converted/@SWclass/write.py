# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\write.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function check = write(a,fid,buslist)
# write slack buses

check = 0

if not a.n, return, end

# filter slack buses using bus list
idx = []
for i in range(1, a.n+1):
  jdx = find(buslist == a.bus(i)*a.u(i))
  if not isempty(jdx), idx = [idx; i]; end

if isempty(idx), return, end

data = a.con(idx,:)
jdx = find(data(:,12))
if isempty(jdx), data(1,12) = 1; end

# write SW data
check = 1
fprintf(fid,'SW.con = [ SW.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],data');
fprintf(fid,'   ];\n\n')
