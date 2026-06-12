# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PLclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

x = cell(4,1)
y = cell(4,1)
s = cell(4,1)

x{1} = [-1 -1 1 1 -1]
y{1} = [-1 1 1 -1 -1]
s{1} = 'k'

x{2} = [0 0]
y{2} = [-0.3 0.3]
s{2} = 'b'

x{3} = [-0.3 -0.7 -0.3 -0.7]
y{3} = [-0.3 -0.3 0.3 0.3]
s{3} = 'b'

x{4} = [0.3 0.3 0.6 0.7 0.7 0.6 0.3]
y{4} = [-0.3 0.3 0.3 0.2 0.1 0 0]
s{4} = 'b'
