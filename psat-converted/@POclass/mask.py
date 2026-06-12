# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@POclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

[xp,yp] = fm_draw('P','Pod',orient)
[xo,yo] = fm_draw('O','Pod',orient)
[xd,yd] = fm_draw('D','Pod',orient)

x = cell(4,1)
y = cell(4,1)
s = cell(4,1)

x{1} = [-1.8 4.1 4.1 -1.8 -1.8]
y{1} = [-1.5 -1.5 1.5 1.5 -1.5]
s{1} = 'k'

x{2} = 1.5*xp-0.7
y{2} = 2*yp
s{2} = 'r'

x{3} = 0.7+1.5*xo
y{3} = 2*yo
s{3} = 'r'

x{4} = 3.5+1.5*xd
y{4} = 2*yd
s{4} = 'r'

