# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SWclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

switch values{8}
  
 case 'on'
  
  cx1 = 'plot([0 1 1 0 0],[0 0 1 1 0]), '
  cx2 = 'color(''blue''), '
  cx3 = 'plot([0 1],[0 1],[0 1],[1 0],[0.5 1 0.5 0 0.5],[0 0.5 1 0.5 0])'
    
 case 'off'
  
  cx1 = 'plot(x,y), '
  cx2 = 'color(''blue''), '
  cx3 = 'plot([0.1 0.3 0.5]-0.6,[0.3 -0.3 0.3],0.45*xt+0.1,0.6*yt)'
  

display = [cx1, cx2, cx3]
set_param(object,'MaskDisplay',display)
