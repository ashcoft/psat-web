# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@YPclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
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
   case 'day'
    if len(index) == 2
      a.day(index(2).subs{:}) = val
    else
      a.day = val
   case 'week'
    if len(index) == 2
      a.week(index(2).subs{:}) = val
    else
      a.week = val
   case 'year'
    if len(index) == 2
      a.year(index(2).subs{:}) = val
    else
      a.year = val
   case 'n'
    a.n = val
   case 'd'
    a.d = val
   case 'w'
    a.w = val
   case 'y'
    a.y = val
   case 'len'
    a.len = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
