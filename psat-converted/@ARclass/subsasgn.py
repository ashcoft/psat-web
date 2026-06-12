# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = subsasgn(a,index,val)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'con'
    if len(index) == 2
      a.con(index(2).subs{:}) = val
    else
      a.con = val
   case 'int'
    if len(index) == 2
      a.int(index(2).subs{:}) = val
    else
      a.int = val
   case 'bus'
    if len(index) == 2
      a.bus(index(2).subs{:}) = val
    else
      a.bus = val
   case 'names'
    if len(index) == 2
      a.names(index(2).subs{:}) = val
    else
      a.names = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
   case 'slack'
    if len(index) == 2
      a.slack(index(2).subs{:}) = val
    else
      a.slack = val
