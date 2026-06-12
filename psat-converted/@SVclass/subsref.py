# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SVclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'Be'
    b = a.Be
   case 'bcv'
    b = a.bcv
   case 'vref'
    if len(index) == 2
      b = a.vref(index(2).subs{:})
    else
      b = a.vref
   case 'q'
    if len(index) == 2
      b = a.q(index(2).subs{:})
    else
      b = a.q
   case 'vm'
    b = a.vm
   case 'alpha'
    b = a.alpha
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
