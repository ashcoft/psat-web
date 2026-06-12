# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@YPclass\gams.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [nH,Ch] = gams(a,type)

nH = ''
Ch = struct('val',[],'labels',[],'name','')

switch type
 case 2
  nH = ['H',num2str(a.len)]
 case 4
  nH = 'H1'

if type == 2
  Ch.val = np.zeros((a.len+1,1))
  Ch.val = [0;a.day(:,a.d)]'*a.week(a.w)*a.year(a.y)/1e6;
  Ch.val(1) = Ch.val(2)
  Ch.labels = cell(1,a.len+1)
for idx in range(1, a.len+1+1):
    Ch.labels{idx} = ['H',num2str(idx-1)]
  Ch.name = 'Ch'
elseif type == 4
  Ch.val = [1,1]
  Ch.name = 'Ch'
  Ch.labels = {'H0','H1'}

