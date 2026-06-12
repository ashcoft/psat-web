# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BKclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

display1 = ['plot([1 2 2 1 1],[-1 -1 1 1 -1]),color(''red''),', ...
            'plot([1 2],[-1 1],[2 1],[-1 1])']

display2 = ['plot([1 2 2 1 1],[-1 -1 1 1 -1])']

type = values{2}

switch type
 case 'on',  set_param(object,'MaskDisplay',display1)
 case 'off', set_param(object,'MaskDisplay',display2)
