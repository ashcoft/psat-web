# Module: psat.gui.fm_annealing
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [nu,nl,pmu_test, I_idx, pseudoi, ok] = fm_annealing(rangoH,ntest,pmu_test,nu,nl,hdl_nob,zeroinj)
# FM_ANNEALING define the Simulated  Aneealing method for
#              PMU placement
#
# (...) = FM_ANNEALING(...)
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

global Bus Line Fig

if nu == 1; ok = 1; return; end

E = Bus.n - rangoH
T = 15
a = 0.0002
if Bus.n < 20, a = 0.002; end
M = min(5000, round(a*nchoosek(Bus.n,ntest)))
if M == 0, M = 1; end

for qwerty in range(1, 40+1):
for ytrewq in range(1, M+1):
    pmusel = randperm(ntest)
    selected_pmu = pmu_test(pmusel(1))
    pmu_test_new = pmu_test(find(pmu_test != selected_pmu))

    bus_mis = Bus.int(pmu_test)
    n_mis = len(pmu_test)
    bus_cal = Bus.a
    cal_con = getidx(Bus,0)
    a = []
for ii in range(1, len(pmu_test)+1):
      a = [a; find(bus_cal == bus_mis(ii))]
    if not isempty(a)
      bus_cal(a) = []
      cal_con(a) = []
    n_cal = len(bus_cal)
    linee = [Line.fr, Line.to]

    while 1
      nonpmusel = randperm(n_cal)
      selected_non_pmu = cal_con(nonpmusel(1))
      i_idx = fm_iidx(selected_non_pmu,linee)
      if len(i_idx(:,1)) > 1
        pmu_test_new = [pmu_test_new; selected_non_pmu]
        break

    I_idx = []
    nodi = []
    pseudoi = 0

for ijk in range(1, ntest+1):
      i_idx = fm_iidx(pmu_test_new(ijk),linee)
      I_idx = [I_idx; i_idx]
# nodi osservabili dal primo PMU
      nodi_oss = [i_idx(:,4);pmu_test_new(ijk)]
      nodi = [nodi; nodi_oss]
#linee(i_idx(:,2),[1 2]) = zeros(length(nodi_oss)-1,2);

# determinazione delle pseudo-correnti  determinate con la
# legge di Kirchhoff per le correnti
# ed eliminazione dei nodi di cui si puo' determinare la
# tensione con la legge di Ohm
# determinazione delle pseudo-correnti nelle linee ai cui
# estremi sono note le tensioni
for ii in range(1, len(nodi)+1):
      I_idx_from = find(linee(:,1) == nodi(ii))
      if not isempty(I_idx_from)
        I_idx_to = []
for jj in range(1, len(I_idx_from)+1):
          if not isempty(find(nodi == linee(I_idx_from(jj),2)))
            I_idx_to = [I_idx_to; I_idx_from(jj)]
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

# ricerca di pseudo-correnti che possono essere
# misurate con il nodo aggiunto
for ii in range(1, len(nodi)+1):
            I_idx_from = find(linee(:,1) == nodi(ii))
            if not isempty(I_idx_from)
              I_idx_to = []
for jj in range(1, len(I_idx_from)+1):
                if not isempty(find(nodi == linee(I_idx_from(jj),2)))
                  I_idx_to = [I_idx_to; I_idx_from(jj)]
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

    nodi_ord = sort(nodi)
    num_nodi = len(nodi)
    nodi_el = []
for jjj in range(1, num_nodi+1):
      nodi_el = [nodi_el; jjj+find(nodi_ord([jjj+1:num_nodi]) == ...
                                   nodi_ord(jjj))]
    nodi_ord(nodi_el) = []


    if len(nodi_ord) == Bus.n
      I_idx(:,1) = [1:len(I_idx(:,1))]';
      [Vest, angest, rangoH] = fm_lssest(pmu_test_new, I_idx,0)
      Enew = Bus.n - rangoH
    else
      Enew = Bus.n - len(nodi_ord)
    if ishandle(Fig.pmu)
      set(hdl_nob,'String',int2str(Enew))
      drawnow
    if Enew == 0
      nu = ntest
      pmu_test = pmu_test_new
      ok = 1
      return
    deltaE = Enew - E
    if deltaE > 0
      probE = exp(-deltaE/T)
#nprobE = 1-probE;
#pE = [ones(1,round(probE*1e5)), zeros(1,round(nprobE*1e5))];
#p = randperm(length(pE));
#pE = pE(p);
#if pE(1)
      if rand <= probE
        pmu_test = pmu_test_new
        E = Enew
    else
      pmu_test = pmu_test_new
      E = Enew

  T = 0.879*T
nl = ntest
ok = 0