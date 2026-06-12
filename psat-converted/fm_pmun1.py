# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_pmun1.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function pmuloc = fm_pmun1
# FM_PMUN1 routine for PMU placement with N-1 contingency
#          criterion in case of device outage
#
# PMU = FM_PMUN1
#     PMU number and position of PMUs
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

fm_var

if isempty(PMU.report)
  fm_pmuloc

nsets = len(PMU.report.Matrix)-2
nconf = 0
pmuloc = []
for i in range(1, nsets+1):
  nconf = nconf + size(PMU.report.Matrix{i+2,1},2)

if nconf == 1
  pmuloc = PMU.report.Matrix{3,1}(Bus.a,1)
else
for i in range(1, nsets+1):
    pmuloc = [pmuloc; PMU.report.Matrix{i+2,1}(Bus.a,:)]

size_pmu = size(pmuloc)

# inizio della routine per determinare
# l'osservabilita' della rete con un
# criterio n-1 sui PMU

gold = DAE.g
fm_call('series')
roundg = round(abs(DAE.g)/Settings.lftol)*Settings.lftol
DAE.g = gold

zeroinj = roundg(Bus.a)+roundg(Bus.v)

for set_i in range(1, size_pmu(2)+1):
  fm_print(['Set of PMU #',num2str(set_i)])
  fm_print(' ')
  pmu_idx = find(pmuloc(:,set_i))
  pmu_num = len(pmu_idx)

for pmu_out in range(0, pmu_num+1):

# vettore contenente i bus in cui si collocano i PMU
    pmu_con = []
# indice delle correnti misurate:
# I_idx => [#corrente, #linea, from bus, to bus, sign]
    I_idx = []

# conteggio delle connessioni e ordinamento dei nodi
    nodi = [Line.fr; Line.to]
    n_link = np.zeros((Bus.n,2))
for i in range(1, Bus.n+1):
      a = find(nodi == getidx(Bus,i))
      n_link(i,:) = [getidx(Bus,i), len(a)]
    [y,i] = sort(n_link(:,2))
    n_link = n_link(i,:)
    linee = nodi
    pseudoi = 0
    nodi = []

    pmu_try = pmu_idx
    if pmu_out, pmu_try(pmu_out) = []; end
    uno = 0; if pmu_out, uno = 1; end
for pmu_i in range(1, pmu_num-uno+1):

# metti PMU nel nodo non osservabile pi interconnesso
      pmu_con = [pmu_con; getidx(Bus,pmu_try(pmu_i))]
      i_idx = fm_iidx(pmu_con(end),linee)

      if not isempty(i_idx)
        I_idx = [I_idx; i_idx]
# nodi osservabili dal PMU
        nodi_oss = [i_idx(:,4);pmu_con(end)]
        nodi = [nodi; nodi_oss]
        linee(i_idx(:,2),[1 2]) = np.zeros((len(nodi_oss)-1,2))

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
        pi_idx = [api, bpi, cpi]
        linee(pi_idx(:,2),[1 2]) = np.zeros((len(pi_idx(:,1)),2))
        I_idx = [I_idx; pi_idx]
        pseudoi = pseudoi + len(pi_idx(:,1))

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
# dopo l'aggiunta di un nuovo nodo misurato bisogna
# ricontrollare tutti i nodi
          count = 1

# ricerca di pseudo-correnti che possono essere misurate
# con il nodo aggiunto
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
              pi_idx = [api, bpi, cpi]
              linee(pi_idx(:,2),[1 2]) = np.zeros((len(pi_idx(:,1)),2))
              I_idx = [I_idx; pi_idx]
              pseudoi = pseudoi + len(pi_idx(:,1))

        else
          count = count + 1
      else
        count = count + 1

    a = []
    for i = 1:len(nodi); a = [a; find(n_link(:,1) == nodi(i))]; end
    if not isempty(a); n_link(a,:) = []; end

    if pmu_out,
      fm_print(['Without PMU at bus ', ...
            fvar(Bus.names{pmu_idx(pmu_out)},12), ...
            ' Number of not osservable buses ', ...
            num2str(len(n_link(:,1)))])
    else
      fm_print(['With all PMU''s  Number of not osservable buses ', ...
            num2str(len(n_link(:,1)))])
  fm_print(' ')
