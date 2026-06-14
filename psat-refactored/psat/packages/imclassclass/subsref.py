# Module: psat.packages.imclassclass.subsref
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
   case 'dat'
    if len(index) == 2
      b = a.dat(index(2).subs{:})
    else
      b = a.dat
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'z'
    if len(index) == 2
      b = a.z(index(2).subs{:})
    else
      b = a.z
   case 'bus'
    b = a.bus
   case 'vbus'
    b = a.vbus
   case 'n'
    b = a.n
   case 'slip'
    b = a.slip
   case 'e1r'
    b = a.e1r
   case 'e1m'
    b = a.e1m
   case 'e2r'
    b = a.e2r
   case 'e2m'
    b = a.e2m
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format