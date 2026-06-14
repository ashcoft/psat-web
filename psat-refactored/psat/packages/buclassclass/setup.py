# Module: psat.packages.buclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global DAE Settings Varname

# check buses
if isempty(a.con)
  fm_print(['The data file does not seem to be in a valid ', ...
           'format: no bus found.'])
  Settings.ok = 0
  a.store = []
  return
a.n = len(a.con(:,1))
a.a = [1:a.n]';
a.v = a.a + a.n
# set up internal bus numbers for second indexing of buses
a.int(round(a.con(:,1)),1) = a.a

# check bus voltage rates
if len(a.con(1,:)) < 2
  fm_print('No voltage rates found in Bus data.',2)
  Settings.ok = 0
  return
idx = find(a.con(:,2) == 0)
if not isempty(idx)
  fm_print('Some Bus voltage rate is zero! 1 kV will be used.')
  a.con(idx,2) = 1

# defining bus names
if isfield(Varname,'bus')
# backward compatibility
  if not isempty(Varname.bus)
    a.names = Varname.bus
  Varname = rmfield(Varname,'bus')
if len(a.names) != a.n
  fm_print('Bus names does not match bus number.',2)
  a.names = ''
if isempty(a.names)
  a.names = fm_strjoin({'Bus '},int2str(a.con(:,1)))

DAE.m = 2*a.n
DAE.y = np.zeros((DAE.m,1))
DAE.g = np.zeros((DAE.m,1))
DAE.Gy = sparse(DAE.m,DAE.m)

if len(a.con(1,:)) == 2
  a.con = [a.con, np.ones((a.n,1)])
if len(a.con(1,:)) == 3
  a.con = [a.con, np.zeros((a.n,1)])
if len(a.con(1,:)) == 4
  a.con = [a.con, np.ones((a.n,1)])
if len(a.con(1,:)) == 5
  a.con = [a.con, np.ones((a.n,1)])

# check voltage magnitudes
Vlow  = find(a.con(:,3) < 0.5)
Vhigh = find(a.con(:,3) > 1.5)
if not isempty(Vlow),
  fm_print(['Warning: some initial guess voltage magnitudes are too low.'])
if not isempty(Vhigh),
  fm_print(['Warning: some initial guess voltage magnitudes are too high.'])
DAE.y(a.v) = a.con(:,3)

# check voltage phases
aref = min(abs(a.con(:,4)))
alow  = find(a.con(:,4)-aref < -1.5708)
ahigh = find(a.con(:,4)-aref >  1.5708)
if not isempty(alow),
  fm_print(['Warning: some initial guess voltage phases are too low.'])
if not isempty(ahigh),
  fm_print(['Warning: some initial guess voltage phases are too high.'])
DAE.y(a.a) = a.con(:,4)

a.Pl = np.zeros((a.n,1))
a.Ql = np.zeros((a.n,1))
a.Pg = np.zeros((a.n,1))
a.Qg = np.zeros((a.n,1))
a.store = a.con