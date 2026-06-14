# Module: psat.packages.ccclassclass.subsref
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
   case 'q1'
    if len(index) == 2
      b = a.q1(index(2).subs{:})
    else
      b = a.q1
   case 'q'
    if len(index) == 2
      b = a.q(index(2).subs{:})
    else
      b = a.q
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'bus'
    b = a.bus
   case 'vbus'
    b = a.vbus
   case 'n'
    b = a.n
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format