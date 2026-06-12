# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_mintree.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [pmuloc, pmunum] = fm_mintree(zeroinj, hdl_pmu,hdl_nob)
# FM_MINTREE compute minimum spanning tree of the current network
#            (for PMU placement routines)
#
# (...) = FM_MINTREE(...)
#
# This function is generally called by FM_PMULOC
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Bus Line Fig Settings

A = sparse(Bus.n,Bus.n)
pmuloc = sparse(Bus.n,Bus.n)

for i in range(1, Bus.n+1):
  nonzero = find(Line.Y(i,:))
  A(i,nonzero) = np.ones((1,len(nonzero)))

p = symrcm(A)
r(p) = 1:Bus.n
A = A(p,p)

spanning = getnp.zeros((Bus))
pmunum = getnp.zeros((Bus))

for i in range(1, Bus.n+1):
  spanning = A(i,:)
  pmuloc(i,i) = 1
  pmunum(i) = 1
  sumspan = sum(spanning)
  while sumspan < Bus.n
for j in range(1, Bus.n+1):
      B(j) = sum(full(spanning | A(j,:)))
    [value, indice] = max(B)
    spanning = spanning | A(indice,:)
    pmunum(i) = pmunum(i) + 1
    pmuloc(i,indice) = 1
    sumspan = sum(spanning)
    if ishandle(Fig.pmu)
      set(hdl_pmu,'String',int2str(pmunum(i)))
      set(hdl_nob,'String',int2str(Bus.n-sumspan))
      drawnow

pmuloc = pmuloc(r,r)
pmunum = pmunum(r)