# Module: psat.packages.wnclassclass.subsasgn
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
   case 'vw'
    a.vw = val
   case 'vwa'
    a.vwa = val
   case 'n'
    a.n = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
   case 'speed'
    if len(index) == 2
      switch index(2).subs
       case 'vw'
        a.speed.vw = val
       case 'time'
        a.speed.time = val
    elseif len(index) == 3
      switch index(3).subs
       case 'vw'
        a.speed(index(2).subs{:}).vw = val
       case 'time'
        a.speed(index(2).subs{:}).time = val