# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PQclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
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
   case 'bus'
    a.bus = val
   case 'gen'
    a.gen = val
   case 'shunt'
    a.shunt = val
   case 'n'
    a.n = val
   case 'P0'
    if len(index) == 2
      a.P0(index(2).subs{:}) = val
    else
      a.P0 = val
   case 'Q0'
    if len(index) == 2
      a.Q0(index(2).subs{:}) = val
    else
      a.Q0 = val
   case 'u'
    if len(index) == 2
      a.u(index(2).subs{:}) = val
    else
      a.u = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
