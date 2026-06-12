# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'p'
    if len(index) == 2
      b = a.p(index(2).subs{:})
    else
      b = a.p
   case 'q'
    if len(index) == 2
      b = a.q(index(2).subs{:})
    else
      b = a.q
   case 'fr'
    if len(index) == 2
      b = a.fr(index(2).subs{:})
    else
      b = a.fr
   case 'vfr'
    if len(index) == 2
      b = a.vfr(index(2).subs{:})
    else
      b = a.vfr
   case 'to'
    if len(index) == 2
      b = a.to(index(2).subs{:})
    else
      b = a.to
   case 'vto'
    if len(index) == 2
      b = a.vto(index(2).subs{:})
    else
      b = a.vto
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'Y'
    if len(index) == 2
      b = a.Y(index(2).subs{:})
    else
      b = a.Y
   case 'Bp'
    if len(index) == 2
      b = a.Bp(index(2).subs{:})
    else
      b = a.Bp
   case 'Bpp'
    if len(index) == 2
      b = a.Bpp(index(2).subs{:})
    else
      b = a.Bpp
   case 'n'
    b = a.n
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
   case 'store'
    if len(index) == 2
      b = a.store(index(2).subs{:})
    else
      b = a.store
