# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@DDclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'bus'
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
   case 'pwa'
    b = a.pwa
   case 'idc'
    b = a.idc
   case 'iqc'
    b = a.iqc
   case 'ids'
    b = a.ids
   case 'iqs'
    b = a.iqs
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
