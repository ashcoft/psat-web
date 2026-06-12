# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [enables,prompts] = block(a,object,values,enables,prompts)

display = 'plot(xc,yc), color(''blue''), text(-0.5,0.1,'

num = str2num(values{2})
type = get_param(object,'MaskType')

blocks = find_system(gcs,'MaskType',type)
idx = strmatch(object,blocks,'exact')
blocks(idx) = []

id = np.zeros((1,len(blocks)))
for i in range(1, len(blocks)+1):
 values = get_param(blocks{i},'MaskValues')
 id(i) = str2num(values{2})

uid = unique(id)
if len(uid) < len(id)
  fm_print(['There are multiple defined ',type(1:end-1),' Id Numbers'],2)

idx = find(uid == num)
if isempty(idx)
  num = num2str(num)
else
  fm_print(['The ', type(1:end-1),' Id ',num2str(num),' is already taken.'])
  nid = 1:len(uid)
  idx = find(nid < uid)
  if isempty(idx)
    num = num2str(len(uid)+1)
  else
    num = num2str(nid(idx(1)))
  fm_print(['PSAT will use ',num,' as ',type(1:end-1),' Id.'])
  values = get_param(object,'MaskValues')
  values{2} = num
  set_param(object,'MaskValues',values)

switch type
 case 'Areas',  set_param(object,'MaskDisplay',[display,'''Area ',num,''')'])
 case 'Regions', set_param(object,'MaskDisplay',[display,'''Region ',num,''')'])

switch values{1}
 case '0', enables{3} = 'on'
 case '1', enables{3} = 'off'
