# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@HVclass\block.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [enables,prompts] = block(a,object,values,enables,prompts)

type = values{11}
switch type
 case 'Voltage_control'
  prompts{10} = ['Reference dc voltage limits (Vr_max, Vr_min, Vi_max, ' ...
                 'Vi_min) [p.u.]']
 otherwise
  prompts{10} = ['Reference dc current limits (Ir_max, Ir_min, Ii_max, ' ...
                 'Ii_min) [p.u.]']
