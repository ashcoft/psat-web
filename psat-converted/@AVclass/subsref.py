# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@AVclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'bus'
    if len(index) == 2
      b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 'vref'
    if len(index) == 2
      b = a.vref(index(2).subs{:})
    else
      b = a.vref
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'syn'
    if len(index) == 2
      b = a.syn(index(2).subs{:})
    else
      b = a.syn
   case 'vbus'
    b = a.vbus
   case 'n'
    b = a.n
   case 'vf'
    b = a.vf
   case 'vfd'
    b = a.vfd
   case 'vm'
    b = a.vm
   case 'vr1'
    b = a.vr1
   case 'vr2'
    b = a.vr2
   case 'vr3'
    b = a.vr3
   case 'vref0'
    if len(index) == 2
      b = a.vref0(index(2).subs{:})
    else
      b = a.vref0
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
