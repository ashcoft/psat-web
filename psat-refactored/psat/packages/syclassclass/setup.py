# Module: psat.packages.syclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
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

ncol = len(a.con(1,:))
switch ncol
 case 19
  a.con = [a.con,np.zeros((a.n,2),np.ones((a.n,2),np.zeros((a.n,4),np.ones((a.n,1)]))
 case 20
  a.con = [a.con,np.zeros((a.n,1),np.ones((a.n,2),np.zeros((a.n,4),np.ones((a.n,1)]))
 case 21
  a.con = [a.con,np.ones((a.n,2),np.zeros((a.n,4),np.ones((a.n,1)]))
 case 22
  a.con = [a.con,np.ones((a.n,1),np.zeros((a.n,4),np.ones((a.n,1)]))
 case 23
  a.con = [a.con,np.zeros((a.n,4),np.ones((a.n,1)])
 case 24
  a.con = [a.con,np.zeros((a.n,3),np.ones((a.n,1)])
 case 25
  a.con = [a.con,np.zeros((a.n,2),np.ones((a.n,1)])
 case 26
  a.con = [a.con,np.zeros((a.n,1),np.ones((a.n,1)])
 case 27
  a.con(:,28) = a.con(:,27)
  a.con(:,27) = np.ones((a.n,1))

if len(a.con(1,:)) < a.ncol
  a.u = np.ones((a.n,1))
else
  a.u = a.con(:,a.ncol)

a.n = len(a.con(:,1))
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))
a.u = a.u.*fm_genstatus(a.bus)

a.pm0 = np.zeros((a.n,1))
a.vf0 = np.zeros((a.n,1))
a.J11 = np.zeros((a.n,1))
a.J12 = np.zeros((a.n,1))
a.J21 = np.zeros((a.n,1))
a.J22 = np.zeros((a.n,1))

a.store = a.con