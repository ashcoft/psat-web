# Module: psat.gui.fm_pmurec
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [bus_pmu, bus2] = fm_pmurec(bus1,bus2,bus0)
# FM_PMUREC routine for PMU placement
#
# (...) = FM_PMUREC(...)
#
# This routine is called by FM_PMULOC
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Bus Line

b = busidx(Line,bus1)
if len(b) == 1
  bus_pmu = b
  bus2(Bus.int(b)) = 1
  return

b1 = find(not bus2(Bus.int(b)))
if isempty(b1)
  bus_pmu = []
  return
else
  b = sort(b(b1))

bus2(Bus.int(b)) = np.ones((len(b),1))

bb = []

for k in range(1, len(b)+1):
  abb = busidx(Line,b(k))
  abb = abb(find(not bus2(Bus.int(abb))))
  bb = [bb; abb]

if isempty(bb); bus_pmu = []; return; end

bb = sort(bb)
num_bus = len(bb)
nodi_el = []
for jjj in range(1, num_bus-1+1):
  nodi_el = [nodi_el; jjj + find(bb([jjj+1:num_bus]) == bb(jjj))]
bb(nodi_el) = []
bb = bb(find(not bus2(Bus.int(bb))))
bus2(Bus.int(bb)) = np.ones((len(bb),1))

bus_pmu = sort(bb)