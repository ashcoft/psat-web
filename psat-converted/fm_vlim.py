# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_vlim.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function  [Vx,Vn] = fm_vlim(maxV,minV)
# FM_VLIM determines max and min bus voltages
#
# [VMAX,VMIN] = FM_VLIM(MAXV,MINV)
#       MAXV -> default max voltage
#       MINV -> default min voltage
#       VMAX -> vector of max bus voltages
#       VMIN -> vector of min bus voltages
#
#Author:    Federico Milano
#Date:      26-Dic-2005
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
#Copyright (C) 2002-2016 Federico Milano

global Bus SW PV PQ

Vn = getnp.zeros((Bus))
Vx = getnp.zeros((Bus))

if PQ.n
  Vn(PQ.bus) = vmin(PQ)
  Vx(PQ.bus) = vmax(PQ)

if PV.n
  Vn(PV.bus) = vmin(PV)
  Vx(PV.bus) = vmax(PV)

if SW.n
  Vn(SW.bus) = vmin(SW)
  Vx(SW.bus) = vmax(SW)

Vn(find(Vn == 0)) = minV
Vx(find(Vx == 0)) = maxV