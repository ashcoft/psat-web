# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@WNclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'vw'
    if len(index) == 2
      b = a.vw(index(2).subs{:})
    else
      b = a.vw
   case 'ws'
    if len(index) == 2
      b = a.ws(index(2).subs{:})
    else
      b = a.ws
   case 'vwa'
    b = a.vwa
   case 'n'
    b = a.n
   case 'store'
    b = a.store
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
   case 'speed'
    if len(index) == 2
      switch index(2).subs
       case 'vw'
        b = a.speed.vw
       case 'time'
        b = a.speed.time
    elseif len(index) == 3
      switch index(3).subs
       case 'vw'
        b = a.speed(index(2).subs{:}).vw
       case 'time'
        b = a.speed(index(2).subs{:}).time
    else
      b = a.speed
