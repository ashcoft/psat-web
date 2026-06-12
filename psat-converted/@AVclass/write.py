# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\write.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = write(a,fid,synlist,offset)
# write AVR data
idx = []

if not a.n, return, end

# filter AVRs using synchronous machine list
idx = []
sdx = []
for i in range(1, a.n+1):
  jdx = find(synlist == a.syn(i)*a.u(i))
  if not isempty(jdx), idx = [idx; i]; end
  sdx = [sdx; jdx]

if isempty(idx), return, end

data = a.con(idx,:)
data(:,1) = sdx + offset

# write AVR data
fprintf(fid,'Exc.con = [ Exc.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],data');
fprintf(fid,'   ];\n\n')
