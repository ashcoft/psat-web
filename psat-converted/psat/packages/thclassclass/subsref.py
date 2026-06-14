# Module: psat.packages.thclassclass.subsref
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
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'bus'
    b = a.bus
   case 'n'
    b = a.n
   case 'T'
    b = a.T
   case 'x'
    b = a.x
   case 'G'
    b = a.G
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format