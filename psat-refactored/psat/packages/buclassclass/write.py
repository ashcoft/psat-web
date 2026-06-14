# Module: psat.packages.buclassclass.write
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def write(a, fid, buslist):

# write bus data

fprintf(fid,'Bus.con = [ Bus.con; ...\n')
fprintf(fid,['   ',a.format,';\n'],a.con(buslist,:)');
fprintf(fid,'   ];\n\n')

fprintf(fid,'Bus.names = [ Bus.names; { ...\n')
for i in range(1, len(buslist)+1):
  fprintf(fid,'    ''%s'';\n',a.names{buslist(i)})
fprintf(fid,'   }];\n\n')