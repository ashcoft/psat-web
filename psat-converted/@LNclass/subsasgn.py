# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
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
   case 'u'
    if len(index) == 2
      a.u(index(2).subs{:}) = val
    else
      a.u = val
   case 'Y'
    if len(index) == 2
      a.Y(index(2).subs{:}) = val
    else
      a.Y = val
   case 'p'
    if len(index) == 2
      a.p(index(2).subs{:}) = val
    else
      a.p = val
   case 'q'
    if len(index) == 2
      a.q(index(2).subs{:}) = val
    else
      a.q = val
   case 'fr'
    if len(index) == 2
      a.fr(index(2).subs{:}) = val
    else
      a.fr = val
   case 'to'
    if len(index) == 2
      a.to(index(2).subs{:}) = val
    else
      a.to = val
   case 'n'
    a.n = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
