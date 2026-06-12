# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
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
   case 'bus'
    a.bus = val
   case 'vbus'
    a.vbus = val
   case 'syn'
    a.syn = val
   case 'vr1'
    a.vr1 = val
   case 'vr2'
    a.vr2 = val
   case 'vr3'
    a.vr3 = val
   case 'vm'
    a.vm = val
   case 'vf'
    a.vf = val
   case 'vref'
    a.vref = val
   case 'vref0'
    if len(index) == 2
      a.vref0(index(2).subs{:}) = val
    else
      a.vref0 = val
   case 'n'
    a.n = val
   case 'u'
    a.u = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
