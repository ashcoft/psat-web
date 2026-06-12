# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@ARclass\setup.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus Settings

switch a.type
 case 'area'
  str = 'Area '
  msg = 'Area names does not match area number.'
  area_buses = getarea(Bus,0,0)
 case 'region'
  str = 'Region '
  msg = 'Region names does not match region number.'
  area_buses = getregion(Bus,0,0)
areas = unique(area_buses)
narea = len(areas)
ndiff = 0
newarea = []
a.store = []

if not isempty(a.con)
  a.n = len(a.con(:,1))
  ncol = len(a.con(1,:))
  if ncol < a.ncol
    a.con = [a.con, np.zeros((a.n,a.ncol-ncol)])
  a.slack = np.zeros((a.n,1))
  sdx = find(a.con(:,2))
  if not isempty(sdx)
    a.slack(sdx) = getint(Bus,a.con(sdx,2))
# check consistency with Bus data
  if a.n != narea
    areaid = a.con(:,1)
    newarea = setdiff(areas,areaid)
    if not isempty(newarea)
      ndiff = len(newarea)
      n = ndiff
      a.n = a.n + n
      a.con = [a.con; [newarea,np.zeros((n,1),100*np.ones((n,1),np.zeros((n,5)]]))
      a.slack = [a.slack; np.zeros((n,1)])
else
# define areas based on Bus data
  ndiff = narea
  newarea = areas
  a.n = narea
  a.con = [areas,np.zeros((a.n,1),100*np.ones((a.n,1),np.zeros((a.n,5)]))
  a.slack = np.zeros((a.n,1))

return
# set up internal area numbers for second indexing of areas
a.int(round(a.con(:,1)),1) = [1:a.n]';

# define bus groups
a.bus = cell(a.n,1)
for i in range(1, a.n+1):
  area_i = find(area_buses == a.con(i,1))
  if not isempty(area_i)
    bus_idx = getidx(Bus,area_i)
    a.bus{i} = getint(Bus,bus_idx)';

# define area names
nnames = len(a.names)
if nnames > 0
  if ndiff
    names = fm_strjoin({str},int2str(newarea))
    a.names = [a.names; names]
  elseif nnames != a.n
    fm_print(msg,2)
    a.names = ''
if isempty(a.names)
  a.names = fm_strjoin({str},int2str(a.con(:,1)))

a.store = a.con
