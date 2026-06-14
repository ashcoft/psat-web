# Module: psat.packages.pqclassclass.simrep
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def simrep(a, blocks, masks, lines):

if not a.n, return, end

typeidx = find(strcmp(masks,'PQ'))

for h in range(1, len(typeidx)+1):
  line_in = find_system(lines,'DstBlockHandle',blocks(typeidx(h)))
  if isempty(line_in)
    line_in = find_system(lines,'SrcBlockHandle',blocks(typeidx(h)))
  v_in  = ['P = ',fvar(a.P0(h),7),' p.u. ->',char(10), ...
      'Q = ',fvar(a.Q0(h),7),' p.u. ->']
  set_param(line_in,'Name',v_in)
