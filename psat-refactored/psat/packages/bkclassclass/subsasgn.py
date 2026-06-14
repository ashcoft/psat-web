# Module: psat.packages.bkclassclass.subsasgn
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
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
   case 'u'
    if len(index) == 2
      a.u(index(2).subs{:}) = val
    else
      a.u = val
   case 't1'
    if len(index) == 2
      a.t1(index(2).subs{:}) = val
    else
      a.t1 = val
   case 't2'
    if len(index) == 2
      a.t2(index(2).subs{:}) = val
    else
      a.t2 = val