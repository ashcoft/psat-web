# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\idnum.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def idnum(a, object, sys):

type = get_param(object,'MaskType')
nameblock = type(1:end-1)
blocks = find_system(sys,'MaskType',type)
maskvalues = get_param(object,'MaskValues')
if isempty(blocks), return, end
if len(blocks) == 1
  maskvalues{1} = '1'
  set_param(object,'MaskValues',maskvalues)
  return
idx = strmatch(object,blocks,'exact')
blocks(idx) = []

id = np.zeros((1,len(blocks)))
for i in range(1, len(blocks)+1):
 values = get_param(blocks{i},'MaskValues')
 id(i) = str2num(values{2})

uid = unique(id)
if len(uid) < len(id)
  fm_print(['There are multiple defined ', nameblock,' Id Numbers'],2)
nid = 1:len(uid)
idx = find(nid < uid)
if isempty(idx)
  num = num2str(len(uid)+1)
else
  num = num2str(nid(idx(1)))

nameblock = [nameblock,' ',num]
maskvalues{2} = num

set_param(object,'MaskDisplay',['plot(xc,yc), color(''blue''), text(-0.5,0.1,''',nameblock,''')'])
set_param(object,'MaskValues',maskvalues)
