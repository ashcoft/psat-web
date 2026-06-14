# Module: psat.packages.pqclassclass.block
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = values{4}
switch type
 case 'on',  enables{3} = 'on'
 case 'off', enables{3} = 'off'
