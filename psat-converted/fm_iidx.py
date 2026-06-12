# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_iidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function  I_idx = fm_iidx(bus_no, Line)
# FM_IIDX find currents injected at a certain bus
#
# I_IDX = FM_IIDX(BUS_NO,Line)
#         BUS_NO bus number
#         Line structure defining network lines
#         I_IDX = [current_#, line_#, from_bus, to_bus, sign]
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

I_idx_fr = find(Line(:,1) == bus_no)
I_idx_to = find(Line(:,2) == bus_no)
n_current = len(I_idx_fr) + len(I_idx_to)
a = [[1:n_current]', [I_idx_fr; I_idx_to]];
b = [Line(I_idx_fr,[1 2]); Line(I_idx_to,[2 1])]
c = [np.ones((len(I_idx_fr),1); -np.ones((len(I_idx_to),1)])
I_idx = [a, b, c]