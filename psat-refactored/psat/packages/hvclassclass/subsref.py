# Module: psat.packages.hvclassclass.subsref
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
   case 'dat'
    if len(index) == 2
      b = a.dat(index(2).subs{:})
    else
      b = a.dat
   case 'u'
    if len(index) == 2
      b = a.u(index(2).subs{:})
    else
      b = a.u
   case 'bus1'
    b = a.bus1
   case 'bus2'
    b = a.bus2
   case 'v1'
    b = a.v1
   case 'v2'
    b = a.v2
   case 'Idc'
    b = a.Idc
   case 'xr'
    b = a.xr
   case 'xi'
    b = a.xi
   case 'cosa'
    b = a.cosa
   case 'cosg'
    b = a.cosg
   case 'phir'
    b = a.phir
   case 'phii'
    b = a.phii
   case 'Vrdc'
    b = a.Vrdc
   case 'Vidc'
    b = a.Vidc
   case 'yr'
    b = a.yr
   case 'yi'
    b = a.yi
   case 'n'
    b = a.n
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format