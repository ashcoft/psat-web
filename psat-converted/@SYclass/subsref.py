# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SYclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'vf0'
    if len(index) == 2
      b = a.vf0(index(2).subs{:})
    else
      b = a.vf0
   case 'pm0'
    if len(index) == 2
      b = a.pm0(index(2).subs{:})
    else
      b = a.pm0
   case 'Pg0'
    if len(index) == 2
      b = a.Pg0(index(2).subs{:})
    else
      b = a.Pg0
   case 'vf'
    if len(index) == 2
      b = a.vf(index(2).subs{:})
    else
      b = a.vf
   case 'pm'
    if len(index) == 2
      b = a.pm(index(2).subs{:})
    else
      b = a.pm
   case 'bus'
    if len(index) == 2
      b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 'vbus'
    b = a.vbus
   case 'n'
    b = a.n
   case 'delta'
    if len(index) == 2
      b = a.delta(index(2).subs{:})
    else
      b = a.delta
   case 'omega'
    if len(index) == 2
      b = a.omega(index(2).subs{:})
    else
      b = a.omega
   case 'e1q'
    b = a.e1q
   case 'e1d'
    b = a.e1d
   case 'e2q'
    b = a.e2q
   case 'e2d'
    b = a.e2d
   case 'psiq'
    b = a.psiq
   case 'psid'
    b = a.psid
   case 'store'
    b = a.store
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
