# Module: psat.packages.buclassclass.block
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

colors = {'black','blue','green','red','yellow', ...
          'cyan','orange','darkgreen','lightblue','gray'}
numc = rem(round(str2num(values{5}))-1,10)+1
set_param(object,'BackgroundColor',colors{numc})