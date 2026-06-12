# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_maskrotate.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [x,y] = fm_maskrotate(x,y,orient)

xt = []
yt = []
for j in range(1, len(x)+1):
  xt = [xt, x{j}]; # #ok<AGROW>
  yt = [yt, y{j}]; # #ok<AGROW>

xmin = min(xt)
xmax = max(xt)
ymin = min(yt)
ymax = max(yt)

for i in range(1, len(x)+1):
  switch orient
   case 'left'
    x{i} = xmax+xmin-x{i}
   case 'up'
    y{i} = ymax+ymin-y{i}
   case 'down'
    y{i} = ymax+ymin-y{i}
    x{i} = xmax+xmin-x{i}

if strcmp(orient,'up')  or  strcmp(orient,'down')
  xold = x
  x = y
  y = xold
