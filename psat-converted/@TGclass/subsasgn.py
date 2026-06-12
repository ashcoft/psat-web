# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\subsasgn.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = subsasgn(a,index,val)
# assigns device properties. properties that are not listed in this
# function cannot be assigned from outside of the class
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
   case 'bus'
    a.bus = val
   case 'syn'
    a.syn = val
   case 'pm'
    a.pm = val
   case 'wref'
    if len(index) == 2
      a.wref(index(2).subs{:}) = val
    else
      a.wref = val
   case 'n'
    a.n = val
   case 'store'
    if len(index) == 2
      a.store(index(2).subs{:}) = val
    else
      a.store = val
   case 'dat1'
    if len(index) == 2
      a.dat1(index(2).subs{:}) = val
    else
      a.dat1 = val
   case 'dat2'
    if len(index) == 2
      a.dat2(index(2).subs{:}) = val
    else
      a.dat2 = val
   case 'dat3'
    if len(index) == 2
      a.dat3(index(2).subs{:}) = val
    else
      a.dat3 = val
   case 'dat4'
    if len(index) == 2
      a.dat4(index(2).subs{:}) = val
    else
      a.dat4 = val
   case 'dat5'
    if len(index) == 2
      a.dat5(index(2).subs{:}) = val
    else
      a.dat5 = val
   case 'dat6'
    if len(index) == 2
      a.dat6(index(2).subs{:}) = val
    else
      a.dat6 = val
