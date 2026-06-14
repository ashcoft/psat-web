# Module: psat.packages.oxclassclass.block
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = values{2}
switch type
 case 'on',  enables([3, 4]) = {'off','off'}
 case 'off', enables([3, 4]) = {'on' ,'on'}