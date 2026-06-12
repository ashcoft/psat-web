# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SUclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
a.bus = getint(Bus,a.con(:,1))

nsup = len(a.con(1,:))
if nsup < 14,
  a.con = [a.con, np.zeros((a.n,14-nsup)])

switch len(a.con(1,:))
 case a.ncol
# All OK!
 case 14
  a.con = [a.con,np.ones((a.n,1),np.zeros((a.n,2),a.con(:,8),a.con(:,8),np.ones((a.n,1)]))
 case 15
  a.con = [a.con,np.zeros((a.n,2),a.con(:,8),a.con(:,8),np.ones((a.n,1)])
 case 16
  a.con = [a.con,np.zeros((a.n,1),a.con(:,8),a.con(:,8),np.ones((a.n,1)])
 case 17
  a.con = [a.con,a.con(:,8),a.con(:,8),np.ones((a.n,1)])
 case 18
  a.con = [a.con,a.con(:,8),np.ones((a.n,1)])
 case 19
  a.con = [a.con,np.ones((a.n,1)])

a.u = a.con(:,a.ncol)
a.store = a.con
