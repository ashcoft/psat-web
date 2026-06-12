# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BUclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = subsasgn(a,index,val)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'n'
    a.n = val
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
   case 'names'
    if len(index) == 2
      a.names(index(2).subs{:}) = val
    else
      a.names = val
   case 'Pg'
    if len(index) == 2
      a.Pg(index(2).subs{:}) = val
    else
      a.Pg = val
   case 'Pl'
    if len(index) == 2
      a.Pl(index(2).subs{:}) = val
    else
      a.Pl = val
   case 'Qg'
    if len(index) == 2
      a.Qg(index(2).subs{:}) = val
    else
      a.Qg = val
   case 'Ql'
    if len(index) == 2
      a.Ql(index(2).subs{:}) = val
    else
      a.Ql = val
   case 'a'
    if len(index) == 2
      a.a(index(2).subs{:}) = val
    else
      a.a = val
   case 'v'
    if len(index) == 2
      a.v(index(2).subs{:}) = val
    else
      a.v = val
   case 'island'
    if len(index) == 2
      a.island(index(2).subs{:}) = val
    else
      a.island = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
