# Module: psat.gui.fm_genstatus
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function  u = fm_genstatus(idx)
# FM_GENSTATUS finds and remove static generators
#
# CHECK = FM_GENSTATUS(IDX)
#       IDX   = bus index where to look for generators
#       U = 0 -> generator off-line (or no generator found)
#       U = 1 -> generator on-line
#
#Author:    Federico Milano
#Date:      24-Aug-2007
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global SW PV PQ

u = np.zeros((len(idx),1))

for i in range(1, len(idx)+1):
  k = idx(i)
  if k <= 0, continue, end
  idx_sw = findbus(SW,k)
  idx_pv = findbus(PV,k)
  idx_pq = findgen(PQ,k)

  if isempty(idx_sw)
    u_sw = 0
  else
    u_sw = SW.u(idx_sw)

  if isempty(idx_pv)
    u_pv = 0
  else
    u_pv = PV.u(idx_pv)

  if isempty(idx_pq)
    u_pq = 0
  else
    u_pq = PQ.u(idx_pq)

  u(i) = u_sw  or  u_pv  or  u_pq