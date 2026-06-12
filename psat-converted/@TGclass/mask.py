# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

[xg,yg] = fm_draw('G','Tg',orient)

x = cell(4,1)
y = cell(4,1)
s = cell(4,1)

x{1} = [-1.8 4.1 4.1 -1.8 -1.8]
y{1} = [-1.5 -1.5 1.5 1.5 -1.5]
s{1} = 'k'

x{2} = [-0.5 -0.5]
y{2} = [-1 1]
s{2} = 'r'

x{3} = [-1.3 0.3]
y{3} = [1 1]
s{3} = 'r'

x{4} = 1.4+xg
y{4} = yg
s{4} = 'r'
