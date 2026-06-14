# Module: psat.packages.ssclassclass.block
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = values{2}
switch type
 case 'constant_power'
  enables([3 7]) = {'on'; 'on'}
 otherwise
  enables([3 7]) = {'off'; 'off'}
