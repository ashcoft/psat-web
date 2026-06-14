# Module: psat.packages.oxclassclass.subsref
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
   case 'v'
    if len(index) == 2
      b = a.v(index(2).subs{:})
    else
      b = a.v
   case 'If'
    if len(index) == 2
      b = a.If(index(2).subs{:})
    else
      b = a.If
   case 'exc'
    if len(index) == 2
      b = a.exc(index(2).subs{:})
    else
      b = a.exc
   case 'n'
    b = a.n
   case 'u'
    b = a.u
   case 'vref'
    b = a.vref
   case 'p'
    b = a.p
   case 'q'
    b = a.q
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format