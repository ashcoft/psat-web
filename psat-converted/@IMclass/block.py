# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@IMclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = str2num(values{2})
idx = [4, 7]

switch type
 case 1, enables(idx) = {'off'; 'off'}
 case 3, enables(idx) = {'on';  'off'}
 case 5, enables(idx) = {'on';  'on'}
