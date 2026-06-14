# Module: psat.packages.psclassclass.subsref
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
   case 'vss'
    if len(index) == 2
      b = a.vss(index(2).subs{:})
    else
      b = a.vss
   case 'bus'
    b = a.bus
   case 'vbus'
    b = a.vbus
   case 'n'
    b = a.n
   case 'syn'
    b = a.syn
   case 'exc'
    b = a.exc
   case 'va'
    b = a.va
   case 'v1'
    b = a.v1
   case 'v2'
    b = a.v2
   case 'v3'
    b = a.v3
   case 's1'
    b = a.s1
   case 'vref'
    b = a.vref
   case 'vf'
    b = a.vf
   case 'p'
    b = a.p
   case 'omega'
    b = a.omega
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format