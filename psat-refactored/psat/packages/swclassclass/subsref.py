# Module: psat.packages.swclassclass.subsref
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
   case 'bus'
    if len(index) == 2
      b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 'vbus'
    if len(index) == 2
      b = a.vbus(index(2).subs{:})
    else
      b = a.vbus
   case 'n'
    b = a.n
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'refbus'
    b = a.refbus
   case 'store'
    b = a.store
   case 'pg'
    b = a.pg
   case 'qg'
    b = a.qg
   case 'dq'
    b = a.dq
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format