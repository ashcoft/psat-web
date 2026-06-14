# Module: psat.packages.mnclassclass.block
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = values{4}
switch type
 case 'on',  prompts{2} = 'Percentage of active  and  reactive powers [%, %]'
 case 'off', prompts{2} = 'Active  and  reactive powers [p.u., p.u.]'