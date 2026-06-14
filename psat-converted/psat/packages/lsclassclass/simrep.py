# Module: psat.packages.lsclassclass.simrep
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def simrep(a, blocks, masks, lines):

if not a.n, return, end

[Ps,Qs,Pr,Qr] = flows(a,[],[],[],[])

lineidx = find(strcmp(masks,'Lines'))

for i in range(1, len(lineidx)+1):
  line_out = find_system(lines,'SrcBlockHandle',blocks(lineidx(i)))
  line_in  = find_system(lines,'DstBlockHandle',blocks(lineidx(i)))
  v_out = [' <- P = ',fvar(Pr(i),7),' p.u.',char(10), ...
      ' <- Q = ',fvar(Qr(i),7),' p.u.']
  v_in  = ['P = ',fvar(Ps(i),7),' p.u. ->',char(10), ...
      'Q = ',fvar(Qs(i),7),' p.u. ->']
  set_param(line_out,'Name',v_out)
  set_param(line_in ,'Name',v_in)