# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BUclass\subsref.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function b = subsref(a,index)

switch index(1).type
 case '.'
  switch index(1).subs
   case 'n'
    b = a.n
   case 'con'
    if len(index) == 2
      b = a.con(index(2).subs{:})
    else
      b = a.con
   case 'int'
    if len(index) == 2
      b = a.int(index(2).subs{:})
    else
      b = a.int
   case 'a'
    if len(index) == 2
      b = a.a(index(2).subs{:})
    else
      b = a.a
   case 'v'
    if len(index) == 2
      b = a.v(index(2).subs{:})
    else
      b = a.v
   case 'names'
    if len(index) == 2
      switch index(2).type
       case '{}'
        b = a.names{index(2).subs{:}}
       case '()'
        b = a.names(index(2).subs{:})
    else
      b = a.names
   case 'Pg'
    if len(index) == 2
      b = a.Pg(index(2).subs{:})
    else
      b = a.Pg
   case 'Pl'
    if len(index) == 2
      b = a.Pl(index(2).subs{:})
    else
      b = a.Pl
   case 'Qg'
    if len(index) == 2
      b = a.Qg(index(2).subs{:})
    else
      b = a.Qg
   case 'Ql'
    if len(index) == 2
      b = a.Ql(index(2).subs{:})
    else
      b = a.Ql
   case 'island'
    if len(index) == 2
      b = a.island(index(2).subs{:})
    else
      b = a.island
   case 'store'
    if len(index) == 2
      b = a.store(index(2).subs{:})
    else
      b = a.store
   case 'ncol'
    b = a.ncol
   case 'format'
    b = a.format
