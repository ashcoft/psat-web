# Module: psat.packages.dsclassclass.subsasgn
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = subsasgn(a,index,val)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'con'
    if len(index) == 2
      a.con(index(2).subs{:}) = val
    else
      a.con = val
   case 'u'
    if len(index) == 2
      a.u(index(2).subs{:}) = val
    else
      a.u = val
   case 'bus'
    a.bus = val
   case 'delta_HP'
    a.delta_HP = val
   case 'omega_HP'
    a.omega_HP = val
   case 'delta_IP'
    a.delta_IP = val
   case 'omega_IP'
    a.omega_IP = val
   case 'delta_LP'
    a.delta_LP = val
   case 'omega_LP'
    a.omega_LP = val
   case 'delta_EX'
    a.delta_EX = val
   case 'omega_EX'
    a.omega_EX = val
   case 'delta'
    a.delta = val
   case 'omega'
    a.omega = val
   case 'pm'
    a.pm = val
   case 'n'
    a.n = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val