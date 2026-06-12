# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SSclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'v0'
    if len(index) == 2
      b = a.v0(index(2).subs{:})
    else
      b = a.v0
   case 'pref'
    if len(index) == 2
      b = a.pref(index(2).subs{:})
    else
      b = a.pref
   case 'bus1'
    b = a.bus1
   case 'bus2'
    b = a.bus2
   case 'line'
    b = a.line
   case 'n'
    b = a.n
   case 'y'
    b = a.y
   case 'xcs'
    b = a.xcs
   case 'Pref'
    b = a.Pref
   case 'V0'
    b = a.V0
   case 'vcs'
    b = a.vcs
   case 'vpi'
    b = a.vpi
   case 'store'
    b = a.store
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
