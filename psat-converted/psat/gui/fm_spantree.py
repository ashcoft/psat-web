# Module: psat.gui.fm_spantree
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [pmu_test, pmu_test2, I_idx, pseudoi, index_pmu, pmunum] = fm_spantree(zeroinj, pmuloc, pmunum, hdl_pmu, hdl_nob)
# FM_SPANTREE routine for determining the spanning tree.  It is
#             used for placing PMUs.
#
# (...) = FM_SPANTREE(...)
#
# This function is called by FM_PMULOC
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Bus Line Fig

# costruzione della matrice di adiacenza di rete
A = np.zeros((Bus.n,Bus.n))
for i in range(1, Bus.n+1):
  nonzero = find(Line.Y(i,:))
  A(i,nonzero) = np.ones((1,len(nonzero)))

# spostamento dei PMU dai nodi in antenna sul nodo adiacente collegato
for i in range(1, len(pmunum)+1):
  idx = find(pmuloc(i,:))
for j in range(1, len(idx)+1):
    if sum(A(idx(j),:)) == 2  and  not zeroinj(idx(j)) == 0
      c = np.zeros((1,Bus.n))
      c(1,idx(j)) = 1
      b = A(idx(j),:) - c
      pmuloc(i,idx(j)) = 0
      pmuloc(i,find(b)) = 1

# determinazione delle misure e delle pseudo misure di corrente
[sortpmu, pmuidx] = sort(pmunum)
pmuloc = pmuloc(pmuidx,:)
pmu_test2 = cell(len(pmunum),1)

for i in range(1, len(pmunum)+1):

  pmu_test_new = getidx(Bus,find(pmuloc(i,:)))
  ntest = len(pmu_test_new)
  if ishandle(Fig.pmu)
    set(hdl_pmu,'String',int2str(ntest))
    drawnow
  linee = [Line.fr, Line.to]

  I_idx = []
  nodi = []
  pseudoi = 0

for ijk in range(1, ntest+1):
    i_idx = fm_iidx(pmu_test_new(ijk),linee)
    I_idx = [I_idx; i_idx]
    nodi_oss = [i_idx(:,4);pmu_test_new(ijk)]
    nodi = [nodi; nodi_oss]
    if ishandle(Fig.pmu)
      set(hdl_nob,'String',int2str(len(nodi)))
      drawnow

  nodi = sort(nodi)
  num_nodi = len(nodi)
  nodi_el = []
for jjj in range(1, num_nodi+1):
    nodi_el = [nodi_el; jjj+find(nodi([jjj+1:num_nodi]) == nodi(jjj))]
  nodi(nodi_el) = []

# determinazione delle pseudo-correnti nelle linee
# ai cui estremi sono note le tensioni
  pi_idx = []
for ii in range(1, len(nodi)+1):
    I_idx_from = find(linee(:,1) == nodi(ii))
    I_idx_to = []
for jj in range(1, len(nodi)+1):
      ifrom = find(linee(I_idx_from,2) == nodi(jj))
      I_idx_to = [I_idx_to; I_idx_from(ifrom)]
    if not isempty(I_idx_to)
      n_current = len(I_idx_to)
      api = [[1:n_current]', I_idx_to];
      bpi = linee(I_idx_to,[1 2])
      cpi = np.ones((len(I_idx_to),1))
      pi_idx = [pi_idx; [api, bpi, cpi]]

  if not isempty(pi_idx)
    linee(pi_idx(:,2),[1 2]) = np.zeros((len(pi_idx(:,1)),2))
    I_idx = [I_idx; pi_idx]
    pseudoi = pseudoi + len(pi_idx(:,1))

# determinazione delle pseudo-correnti  determinate
# con la legge di Kirchhoff per le correnti
# ed eliminazione dei nodi di cui si pu determinare
# la tensione con la legge di Ohm
  count = 1
  while count < len(nodi)
    if zeroinj(Bus.int(nodi(count))) == 0
      I_idx_from = find(linee(:,1) == nodi(count))
      I_idx_to = find(linee(:,2) == nodi(count))
      ncfrom = len(I_idx_from)
      ncto = len(I_idx_to)
      nc = ncfrom + ncto
      if nc == 1
        if ncfrom == 1
          ki_idx = [1, I_idx_from, linee(I_idx_from,[1 2]), 1]
        else
          ki_idx = [1, I_idx_to, linee(I_idx_to,[2 1]), -1]
        linee(ki_idx(2),[1 2]) = np.zeros((len(ki_idx(1)),2))
        I_idx = [I_idx; ki_idx]
        pseudoi = pseudoi + len(ki_idx(1))
        nodi_oss = [nodi_oss; ki_idx(4)]
        nodi = [ki_idx(4); nodi]
        if ishandle(Fig.pmu)
          set(hdl_nob,'String',int2str(len(nodi)))
        drawnow
        count = 1
      else
        count = count + 1
    else
      count = count + 1

  pmu_test2{i,1} = pmu_test_new
  I_idx_test{i,1} = I_idx
  pseudi_test{i,1} = pseudoi


pmu_status = np.zeros((len(pmu_test2),1))
min_pmu = Bus.n
for i in range(1, len(pmu_test2)+1):
  if len(pmu_test2{i,1}) == 1
    pmu_status(i) = 1
    min_pmu = 1

while not all(pmu_status)
  a = find(not pmu_status)
  if ishandle(Fig.pmu)
    set(hdl_pmu,'String',int2str(len(pmu_test2{a(1)})))
    drawnow

  [pmu_test2, I_idx_test, pseudi_test ,pmu_status, min_pmu] = ...
      fm_pmutry(pmu_test2,I_idx_test, pseudi_test,pmu_status, ...
                a(1),hdl_nob,hdl_pmu, min_pmu, zeroinj)

  pmuloc = sparse(len(pmu_test2),Bus.n)
  pmunum = np.zeros((1,len(pmu_test2)))
for i in range(1, len(pmu_test2)+1):
    pmuloc(i,Bus.int(pmu_test2{i})) = np.ones((1,len(pmu_test2{i})))
    pmunum(i) = sum(pmuloc(i,:))

# eliminazione delle configuazioni rindondanti
  pos = 1
  while pos < len(pmunum)
    idx = []
    idxo = 1:pos
for i in range(pos+1, len(pmunum)+1):
      if (pmuloc(pos,:)  and  pmuloc(i,:)) == pmuloc(pos,:)
        idx = [idx, i]
      else
        idxo = [idxo, i]
    pmunum(idx) = []
    pmuloc(idx,:) = []
    pmu_test2(idx) = []
    I_idx_test(idx) = []
    pseudi_test(idx) = []
    pmu_status(idx) = []
    pos = pos + 1
numpmu = Bus.n
numpmuold = Bus.n
index_pmu = []
for i in range(1, len(pmu_test2)+1):
  numpmu = min(numpmu, len(pmu_test2{i,1}))
for i in range(1, len(pmu_test2)+1):
  if numpmu == len(pmu_test2{i,1})
    index_pmu = [index_pmu; i]
pmu_test = pmu_test2(index_pmu)
I_idx = I_idx_test(index_pmu)
pseudoi = pseudi_test(index_pmu)
if ishandle(Fig.pmu)
  set(hdl_pmu,'String',int2str(numpmu))
  set(hdl_nob,'String',int2str(0))
  drawnow