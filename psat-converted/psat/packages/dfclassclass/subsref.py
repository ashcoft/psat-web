# Module: psat.packages.dfclassclass.subsref
# Refactored from psat-converted
# ------------------------------------------------------------------
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
   case 'vref'
    if len(index) == 2
      b = a.vref(index(2).subs{:})
    else
      b = a.vref
   case 'bus'
    if len(index) == 2
      b = a.bus(index(2).subs{:})
    else
      b = a.bus
   case 'vbus'
    b = a.vbus
   case 'wind'
    b = a.wind
   case 'n'
    b = a.n
   case 'theta_p'
    b = a.theta_p
   case 'omega_m'
    b = a.omega_m
   case 'idr'
    b = a.idr
   case 'iqr'
    b = a.iqr
   case 'pwa'
    b = a.pwa
   case 'dat'
    if len(index) == 2
      b = a.dat(index(2).subs{:})
    else
      b = a.dat
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format