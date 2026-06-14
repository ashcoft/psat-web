# Module: psat.packages.bkclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus Line

if isempty(a.con)
  a.store = []
  return

if not isempty(a.con)
  a.line = a.con(:,1)
  a.bus = getint(Bus,a.con(:,2))
  a.n = len(a.con(:,1))
  a.u = a.con(:,6)

# finding breakers that are initially open
  idx = find(not a.u)
  Line.u(a.line(idx)) = 0
# swap intervention times so that first
# intervention will close the breaker
#if ~isempty(idx)
#  a.con(idx,[7 8]) = a.con(idx,[8 7]);
#end
  
# check data consistency
  ncol = size(a.con,2)
  switch ncol
   case 8, a.con = [a.con, np.ones((a.n,2)])
   case 9, a.con = [a.con, np.ones((a.n,1)])
   case 10, #  everything ok!
   otherwise
    fm_print('* * * Error: Breaker data are not complete!')
    a.con = [a.con, np.zeros((a.n, a.ncol-ncol)])
  
# set intervention times
  a.t1 = a.con(find(a.con(:,9)),7)
  a.t2 = a.con(find(a.con(:,10)),8)
  
# intervention times t = 0 are not allowed
  idx = find(a.con(:,7) == 0 & a.con(:,9))
  if not isempty(idx)
    a.con(idx,7) = 1e-6
    a.con(idx,8) = a.con(idx,8)+1e-6
  idx = find(a.con(:,8) == 0 & a.con(:,10))
  if not isempty(idx)
    a.con(idx,8) = 1e-6
    a.con(idx,7) = a.con(idx,7)+1e-6

a.store = a.con