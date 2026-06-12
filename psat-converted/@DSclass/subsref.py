# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DSclass\subsref.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function b = subsref(a,index)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'con'
    if len(index) == 2
      b = a.con(index(2).subs{:})
    else
      b = a.con
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'bus'
    b = a.bus
   case 'n'
    b = a.n
   case 'pm'
    b = a.pm
   case 'delta'
    b = a.delta
   case 'omega'
    b = a.omega
   case 'delta_HP'
    b = a.delta_HP
   case 'omega_HP'
    b = a.omega_HP
   case 'delta_IP'
    b = a.delta_IP
   case 'omega_IP'
    b = a.omega_IP
   case 'delta_LP'
    b = a.delta_LP
   case 'omega_LP'
    b = a.omega_LP
   case 'delta_EX'
    b = a.delta_EX
   case 'omega_EX'
    b = a.omega_EX
   case 'delta'
    b = a.delta
   case 'omega'
    b = a.omega
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
