# Module: psat.packages.ypclassclass.subsref
# Refactored from psat-converted
# ------------------------------------------------------------------
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
   case 'day'
    if len(index) == 2
      b = a.day(index(2).subs{:})
    else
      b = a.day
   case 'week'
    if len(index) == 2
      b = a.week(index(2).subs{:})
    else
      b = a.week
   case 'year'
    if len(index) == 2
      b = a.year(index(2).subs{:})
    else
      b = a.year
   case 'n'
    b = a.n
   case 'd'
    b = a.d
   case 'w'
    b = a.w
   case 'y'
    b = a.y
   case 'len'
    b = a.len
   case 'store'
    b = a.store
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format