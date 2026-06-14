# Module: psat.packages.swclassclass.Fxcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def Fxcall(p, varargin):

global DAE

if not p.n, return, end

if nargin == 1
  type = 'all'
else
  type = varargin{1}

idx = p.vbus(find(p.u))

if isempty(idx),return, end

DAE.Fy(:,idx) = 0
DAE.Gx(idx,:) = 0

if strcmp(type,'onlyq'), return, end

idx = p.bus(find(p.u))
DAE.Fy(:,idx) = 0
DAE.Gx(idx,:) = 0
