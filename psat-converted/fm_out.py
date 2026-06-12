# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_out.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_out(flag, t, k):

# FM_OUT define output variable vector during time domain simulations
#
# FM_OUT(FLAG,T,K)
#   T = actual time
#   K = time step number
#   FLAG = 0 ->  Output Structure Initialization
#	   1 ->  Memory Allocation
#          2 ->  k-th Step Assignment
#          3 ->  Vector Redimensioning
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings Bus DAE Varout Varname Fig

persistent compute_pijs
nb = Bus.n

switch flag

 case 0

  if DAE.n > 5000  or  nb > 5000
    Settings.chunk = 10
  if len(Varname.idx) > Settings.maxvar
    fm_print('No more than 1500 variables will be stored for plotting.')
    Varname.idx = Varname.idx(1:Settings.maxvar)

  Varout.t = np.zeros((Settings.chunk,1))
  Varout.idx = Varname.idx
  idx0 = len(Varout.idx)
  Varout.vars = np.zeros((Settings.chunk,idx0))
  idx1 = DAE.n+DAE.m+2*nb
  if not isempty(find(Varout.idx > idx1))
    compute_pijs = idx1
  else
    compute_pijs = 0
# network visualization
  fm_threed('init')

 case 1

  Varout.t = [Varout.t; np.zeros((Settings.chunk,1)])
  idx0 = len(Varout.idx)
  Varout.vars = [Varout.vars; np.zeros((Settings.chunk,idx0)])

 case 2

  Varout.t(k) = t

  fm_call('series')

  vars = []

  if DAE.n
    vars = DAE.x

  if DAE.m
    vars = [vars; DAE.y; DAE.g(1:2*nb)]

  if compute_pijs

    [ps,qs,pr,qr,bfr,bto] = fm_flows

    ss = abs(ps + i*qs)
    sr = abs(pr + i*qr)
    is = ss./DAE.y(bfr)
    ir = sr./DAE.y(bto)

    vars = [vars; ps; pr; qs; qr; is; ir; ss; sr]


  if Settings.vs
    idx0 = DAE.n+DAE.m+2*nb+8*Settings.nseries
    vars_vs = fm_vs
    idx1 = find(Varout.idx <= idx0)
    idx2 = find(Varout.idx > idx0)
    if not isempty(idx2)
      vars_vs = fm_vs
      Varout.vars(k,:) = [vars(Varout.idx(idx1)); vars_vs(Varout.idx(idx2)-idx0)].';
  else
    Varout.vars(k,:) = vars(Varout.idx).';
  fm_threed('newframe')

 case 3

  Varout.t = Varout.t(1:k)
  Varout.vars = Varout.vars(1:k,:)
  fm_threed('finish')

