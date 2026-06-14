# Module: psat.gui.fm_rmgen
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function  check = fm_rmgen(idx)
# FM_RMGEN finds and remove static generators
#
# CHECK = FM_RMGEN(IDX)
#       IDX   = bus index where to look for generators
#       CHECK = 0 -> no generator found
#       CHECK = 1 -> found generator
#
#Author:    Federico Milano
#Date:      27-Dec-2005
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global SW PV PQ Bus
persistent local_idx

check = 1

if idx == -1
  local_idx = []
  return

if not idx, return, end

if not isempty(local_idx)
  if not isempty(find(local_idx == idx))
    return
  else
    local_idx = [local_idx;idx]
else
  local_idx = [local_idx;idx]

idx_sw = findbus(SW,idx)
idx_pv = findbus(PV,idx)
idx_pq = findgen(PQ,idx)

SW = remove(SW,idx_sw)
PV = remove(PV,idx_pv)
PQ = remove(PQ,idx_pq,'force')

if isempty(idx_pv)  and  isempty(idx_sw)  and  isempty(idx_pq)
  fm_print([' * * Error: No static generator found at bus <', ...
           Bus.names{idx},'>'])
  check = 0