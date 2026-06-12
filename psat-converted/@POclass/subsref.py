# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@POclass\subsref.m  (upstream PSAT, GPL-2.0+)
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
   case 'z'
    b = a.z
   case 'kr'
    b = a.kr
   case 'v1'
    b = a.v1
   case 'v2'
    b = a.v2
   case 'v3'
    b = a.v3
   case 'Vs'
    b = a.Vs
   case 'type'
    b = a.type
   case 'idx'
    b = a.idx
   case 'svc'
    b = a.svc
   case 'statcom'
    b = a.statcom
   case 'sssc'
    b = a.sssc
   case 'tcsc'
    b = a.tcsc
   case 'upfc'
    b = a.upfc
   case 'dfig'
    b = a.dfig
   case 'n'
    b = a.n
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
