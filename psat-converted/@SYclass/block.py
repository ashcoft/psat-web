# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = str2num(values{2})
idx = 11

switch type
 case 2,   enables(idx) = {'off'}
 case 3,   enables(idx) = {'off'}
 case 4,   enables(idx) = {'off'}
 case 5.1, enables(idx) = {'off'}
 case 5.2, enables(idx) = { 'on'}
 case 5.3, enables(idx) = {'off'}
 case 6,   enables(idx) = { 'on'}
 case 8,   enables(idx) = { 'on'}
