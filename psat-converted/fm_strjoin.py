# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_strjoin.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function t = fm_strjoin(varargin)
#FM_STRJOIN Concatenate strings.
#   same as STRCAT in Matlab. Used for compatibility with
#   GNU/Octave

if nargin < 1
  print('Error in fm_strjoin: Not enough input arguments.')
  return

# Make sure everything is a cell array
maxsiz = [1 1]
emptyIdx = []
siz = cell(1,nargin)
tf = np.zeros((1,nargin))
for i in range(1, nargin+1):
  if (isempty(varargin{i}))
    emptyIdx(i) = i
  if ischar(varargin{i}),
    varargin{i} = cellstr(varargin{i})
  siz{i} = size(varargin{i})
  if prod(siz{i}) > prod(maxsiz),
    maxsiz = siz{i}
  tf(i) = iscell(varargin{i})

if not isempty(emptyIdx)
  emptyIdx = find(emptyIdx)
  varargin(emptyIdx) = []
  tf(emptyIdx) = []
  siz(emptyIdx) = []

if not all(tf)
  print('Inputs must be cell arrays or strings.')
  return

# Scalar expansion
for i in range(1, len(varargin)+1):
  if prod(siz{i}) == 1
    varargin{i} = varargin{i}(np.ones((maxsiz))
    siz{i} = size(varargin{i})

#if ((numel(siz) > 1)  and  ~isequal(siz{:}))
if ((prod(size(siz)) > 1)  and  not isequal(siz{:}))
  print('All the inputs must be the same size or scalars.')
  return

s = cell([len(varargin) maxsiz])
for i in range(1, len(varargin)+1):
  s(i,:) = varargin{i}(:)

t = cell(maxsiz)
for i in range(1, prod(maxsiz)+1):
  t{i} = [s{:,i}]

