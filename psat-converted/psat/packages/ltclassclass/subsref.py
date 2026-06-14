# Module: psat.packages.ltclassclass.subsref
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
   case 'delay'
    b = a.delay
   case 'mold'
    b = a.mold
   case 'bus1'
    b = a.bus1
   case 'bus2'
    b = a.bus2
   case 'v1'
    b = a.v1
   case 'v2'
    b = a.v2
   case 'vr'
    b = a.vr
   case 'n'
    b = a.n
   case 'mc'
    b = a.mc
   case 'md'
    b = a.md
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format