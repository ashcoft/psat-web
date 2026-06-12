# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@CLclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'q'
    if len(index) == 2
      b = a.q(index(2).subs{:})
    else
      b = a.q
   case 'vref'
    b = a.vref
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'syn'
    b = a.syn
   case 'cac'
    b = a.cac
   case 'exc'
    b = a.exc
   case 'svc'
    b = a.svc
   case 'n'
    b = a.n
   case 'Vs'
    b = a.Vs
   case 'dVsdQ'
    b = a.dVsdQ
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
