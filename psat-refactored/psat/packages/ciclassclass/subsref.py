# Module: psat.packages.ciclassclass.subsref
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function b = subsref(a,index)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'n'
    b = a.n
   case 'syn'
    if len(index) == 2
      switch index(2).type
       case '{}'
        b = a.syn{index(2).subs{:}}
       case '()'
        b = a.syn(index(2).subs{:})
    else
      b = a.syn
   case 'con'
    b = []
   case 'M'
    b = a.M
   case 'Mtot'
    b = a.Mtot
   case 'delta'
    b = a.delta
   case 'omega'
    b = a.omega
   case 'gen'
    b = a.gen
   case 'dgen'
    b = a.dgen
   case 'wgen'
    b = a.wgen