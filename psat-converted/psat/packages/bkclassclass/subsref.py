# Module: psat.packages.bkclassclass.subsref
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
   case 'store'
    if len(index) == 2
      b = a.store(index(2).subs{:})
    else
      b = a.store
   case 'bus'
    if len(index) == 2
      b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 't1'
    if len(index) == 2
      b = a.t1(index(2).subs{:})
    else
      b = a.t1
   case 't2'
    if len(index) == 2
      b = a.t2(index(2).subs{:})
    else
      b = a.t2
   case 'line'
    if len(index) == 2
      b = a.line(index(2).subs{:})
    else
      b = a.line
   case 'n'
    b = a.n
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format