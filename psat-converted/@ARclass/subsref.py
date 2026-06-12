# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'int'
    if len(index) == 2
      b = a.int(index(2).subs{:})
    else
      b = a.int
   case 'bus'
    if len(index) == 2
      switch index(2).type
       case '{}'
        b = a.bus{index(2).subs{:}}
       case '()'
        b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 'names'
    if len(index) == 2
      switch index(2).type
       case '{}'
        b = a.names{index(2).subs{:}}
       case '()'
        b = a.names(index(2).subs{:})
    else
      b = a.names
   case 'store'
    if len(index) == 2
      b = a.store(index(2).subs{:})
    else
      b = a.store
   case 'slack'
    if len(index) == 2
      b = a.slack(index(2).subs{:})
    else
      b = a.slack
   case 'n'
    b = a.n
   case 'type'
    b = a.type
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
