# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@MNclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

x = cell(2,1)
y = cell(2,1)
s = cell(2,1)

x{1} = [-1 -1 1 1 -1]
y{1} = [-1 1 1 -1 -1]
s{1} = 'k'

x{2} = [-0.35 -0.35 0 0.35 0.35]
y{2} = [-0.35 0.35 0.05 0.35 -0.35]
s{2} = 'b'
