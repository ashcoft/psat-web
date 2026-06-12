# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BUclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

colors = {'black','blue','green','red','yellow', ...
          'cyan','orange','darkgreen','lightblue','gray'}
numc = rem(round(str2num(values{5}))-1,10)+1
set_param(object,'BackgroundColor',colors{numc})
