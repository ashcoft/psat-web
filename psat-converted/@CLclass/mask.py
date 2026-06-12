# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

[xc,yc] = fm_draw('C','Cluster',orient)

x = cell(3,1)
y = cell(3,1)
s = cell(3,1)

x{1} = [1 0 0 1 1]
y{1} = [1 1 0 0 1]
s{1} = 'k'

x{2} = 0.1+0.3*xc
y{2} = 0.5+0.6*yc
s{2} = 'r'

x{3} = 0.6+0.3*xc
y{3} = 0.5+0.6*yc
s{3} = 'r'
