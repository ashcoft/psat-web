# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'store'
    b = a.store
   case 'pq'
    b = a.pq
   case 'newpq'
    b = a.newpq
   case 'qg'
    b = a.qg
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
