# Module: psat.packages.syclassclass.write
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function idx = write(a,fid,buslist)
# write synchronous machine data

global Bus Settings

idx = []

if not a.n, return, end

# filter machines using bus list
idx = []
for i in range(1, a.n+1):
  jdx = find(buslist == a.bus(i)*a.u(i))
  if not isempty(jdx), idx = [idx; i]; end

if isempty(idx), return, end

data = a.con(idx,:)

try
  Vb2old = data(:,3).*data(:,3)
  Vb2new = getkv(Bus,a.bus(idx),2)
  k = Settings.mva*Vb2old./data(:,2)./Vb2new
  i = [6:10, 13:15]
for h in range(1, len(i)+1):
    data(:,i(h))= data(:,i(h))./k
  data(:,18) = Settings.mva*data(:,18)./data(:,2)
  data(:,19) = Settings.mva*data(:,19)./data(:,2)
catch
# nothing to do 

# write Syn data
fprintf(fid,'Syn.con = [ Syn.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],data');
fprintf(fid,'   ];\n\n')