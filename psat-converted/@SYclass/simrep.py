# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\simrep.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def simrep(a, blocks, masks, lines):

global DAE

if not a.n, return, end

typeidx = find(strcmp(masks,'Syn'))

for h in range(1, len(typeidx)+1):
  line_out = find_system(lines,'SrcBlockHandle',blocks(typeidx(h)))
  v_out = ['P = ',fvar(DAE.y(a.p(h)),7),' p.u. ->',char(10) ...
      ,'Q = ',fvar(DAE.y(a.q(h)),7),' p.u. ->']
  set_param(line_out,'Name',v_out)

