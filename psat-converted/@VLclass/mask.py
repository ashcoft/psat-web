# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@VLclass\mask.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y,s] = mask(a,idx,orient,vals)

[xc,yc] = fm_draw('circle','Vltn',orient)

x = cell(2,1)
y = cell(2,1)
s = cell(2,1)

x{1} = xc
y{1} = yc
s{1} = 'k'

x{2} = [0.3 0 -0.3]
y{2} = [0.5 -0.5 0.5]
s{2} = 'b'
