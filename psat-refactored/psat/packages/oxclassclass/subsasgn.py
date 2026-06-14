# Module: psat.packages.oxclassclass.subsasgn
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
   case 'bus'
    a.bus = val
   case 'vbus'
    a.vbus = val
   case 'exc'
    a.exc = val
   case 'v'
    a.v = val
   case 'If'
    a.If = val
   case 'n'
    a.n = val
   case 'u'
    a.u = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val