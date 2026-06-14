# Module: psat.packages.psclassclass.simrep
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def simrep(a, blocks, masks, lines):

global DAE

if not a.n, return, end

typeidx = find(strcmp(masks,'Pss'))

for h in range(1, len(typeidx)+1):
  line_out = find_system(lines,'SrcBlockHandle',blocks(typeidx(h)))
  v_out = ['Vss = ',fvar(DAE.y(a.vss(h)),7),' p.u.']
  set_param(line_out,'Name',v_out)
