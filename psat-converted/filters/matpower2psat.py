# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/filters\matpower2psat.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function check = matpower2psat(filename, pathname)
# MATPOWER2PSAT Matpower 2 PSAT filter
#
# CHECK = MATPOWER2PSAT(FILENAME,PATHNAME)
#       FILENAME name of the file to be converted
#       PATHNAME path of the file to be converted
#
#       CHECK = 1 conversion completed
#       CHECK = 0 problem encountered (no data file created)
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
#*** Contributions ***
#
#Author:    Liulin
#Date:      13-Mar-2003
#Update:    01-May-2004
#           02-Jun-2016
#E-mail:    liu.lin2@zte.com.cn
#
# Copyright (C) 2002-2007 Federico Milano

global Settings Path

check = 0
pathname = [pathname,filesep]

fm_disp
fm_print('Conversion from Matpower Data Format ...')
fm_print(['Source data file "',pathname,filename,'"'])

baseMVA = []
bus = []
gen = []
branch = []
area = []
gencost = []
bus_name = []
try
  cd(pathname)
  mpc = feval(filename(1:end-2))
  baseMVA = mpc.baseMVA
  bus = mpc.bus
  gen = mpc.gen
  branch = mpc.branch
#   area = mpc.area;
#   gencost = mpc.gencost;
  cd(Path.local)
catch
  fm_print(['Something wrong with the file ',pathname,filename])
  fm_print('Conversion Process Interrupted',2)
  return

try
  bus_name = mpc.bus_name
catch
  fm_print(['Bus names undefined. Using default names'])
lasterr('')

try
  if baseMVA == 0, baseMVA = 100; end
  gen(find(gen(:,7)== 0),7) = baseMVA
  bus(:,[3 4 5 6]) = bus(:,[3 4 5 6])/baseMVA
  if sum(bus(:,10)) == 0, bus(:,10) = 1; end
  bus(:,9) = np.pi*bus(:,9)/180
  gen(:,2) = gen(:,2)./gen(:,7)
  gen(:,3) = gen(:,3)./gen(:,7)
  gen(:,4) = gen(:,4)./gen(:,7)
  gen(:,5) = gen(:,5)./gen(:,7)
  gen(:,9) = gen(:,9)./gen(:,7)
  gen(:,10) = gen(:,10)./gen(:,7)
  branch(:,[6 7 8]) = branch(:,[6 7 8])/baseMVA
  if bus,
    if len(bus(1,:)) != 13,
      error('Bus data is not in the standard format'),
  if gen,
    if len(gen(1,:)) != 10,
      error('Generator data is not in the standard format'),
  if branch,
    if len(branch(1,:)) != 11,
      error('Branch data is not in the standard format'),
  if area,
    if len(area(1,:)) != 2,
      error('Area data is not in the standard format'),
  if gencost,
    if len(gencost(1,:)) != max(gencost(:,4)),
      error('Generator cost data is not in the standard format'),
catch
  fm_print(['Error in data file ',pathname,filename])
  fm_print(lasterr)
  fm_print('Conversion process interrupted.',2)
  return

# definition of file name for PSAT data file
extension = findstr(filename,'.')
newfile = ['d_',filename(1:extension(end)-1),'.m']
# open *.m file for writing data
fid = fopen([pathname,newfile], 'wt')
if fid == -1,
  fm_print(['Can''t open file ',pathname,newfile],2),
  return,

# Bus data: Bus.con
# ----------------------------------------------------------------------

nbus = len(bus(:,1))
count = fprintf(fid,['%% ',datestr(now,2), ...
                    ' File data originated from Matpower data file\n'])
count = fprintf(fid,['%% \n\n'])
count = fprintf(fid, 'Bus.con = [ ...\n')
format = '   %4d %8.4g %8.4g %8.4g %4d %4d;\n'
count = fprintf(fid,format,bus(:,[1,10,8,9,7,11])');
count = fprintf(fid,'   ];\n\n')

# Swing Generator data: SW.con
# ----------------------------------------------------------------------

k = find(bus(:,2) == 3)
slackbus = k
if not isempty(k)
  n = len(k)
  h = []
  for i = 1:n, h = [h; find(gen(:,1) == bus(k(i),1))]; end
  if len(h) != n,
    fm_print('Slack bus not found. Conversion process interrupted.',2)
    return
  swline = [bus(k,1),gen(h,7),bus(k,10),gen(h,6),bus(k,9),gen(h,[4,5]), ...
            bus(k,[12,13]),gen(h,2),(gen(h,8) > 0)]
  count = fprintf(fid, 'SW.con = [ ...\n')
  format = ['   %4d',repmat(' %8.4g',1,9),' 1 1 %2u;\n']
  count = fprintf(fid,format,swline');
  count = fprintf(fid,'   ];\n\n')

# PV Generator data: PV.con
# ----------------------------------------------------------------------

#k = find(bus(:,2) == 2);
if not isempty(gen)
  n = len(gen(:,1))
  h = []
for i in range(1, n+1):
    h = [h; find(bus(:,1) == gen(i,1))]
  pvline = [bus(h,1),gen(:,7),bus(h,10),gen(:,[2,6,4,5]), ...
            bus(h,[12,13]),(gen(:,8) > 0)]
  k = find(h == slackbus)
  if k, pvline(k,:) = []; end
  count = fprintf(fid, 'PV.con = [ ...\n')
  format = ['%4d',repmat(' %8.4g',1,8),' 1 %2u;\n']
  count = fprintf(fid,format,pvline');
  count = fprintf(fid,'   ];\n\n')

# Constant Power Load data: PQ.con
# ----------------------------------------------------------------------

k1 = find(bus(:,3) != 0 | bus(:,4) != 0)
# for buses without generators or loads, the Vmin/Vmax must be kept.
k2 = find(bus(:,3) == 0 & bus(:,4) == 0  & bus(:,2) == 1)
count = fprintf(fid, 'PQ.con = [ ...\n')
format = ['%4d ',num2str(baseMVA),repmat(' %8.4g',1,5),' 0 1;\n']
count = fprintf(fid,format,bus([k1;k2],[1,10,3,4,12,13])');
count = fprintf(fid,'   ];\n\n')

# Shunt Impedance data: Shunt.con
# ----------------------------------------------------------------------

k = find(bus(:,5) | bus(:,6))
if not isempty(k)
  count = fprintf(fid, 'Shunt.con = [ ...\n')
  format = ['%4d ',num2str(baseMVA),' %8.4g 60 %8.4g %8.4g 1;\n']
  count = fprintf(fid,format,bus(k,[1 10 5 6])');
  count = fprintf(fid,'   ];\n\n')

# Branch data: Line.con
# ----------------------------------------------------------------------

if not isempty(branch)
  busmax = max(bus(:,1))
  busint = np.zeros((busmax,1))
for i in range(1, nbus+1):
    busint(round(bus(i,1))) = i
  nline = len(branch(:,1))
  Line_con = np.zeros((nline,13))
  Line_con(:,3) = bus(busint(branch(:,1)),10)
  fr = busint(branch(:,1))
  to = busint(branch(:,2))
  Line_con(:,4) = abs(sign(branch(:,9))).*bus(fr,10)./bus(to,10)
  Line_con(:,[1 2 5 6 7 8 9 10 11 12 13]) = ...
      branch(:,[1 2 3 4 5 9 10 6 7 8 11])
  count = fprintf(fid, 'Line.con = [ ...\n')
  format = ['%4d %4d ',num2str(baseMVA),' %8.4g 60 0 ', ...
            repmat(' %8.4g',1,9), ' %2u;\n']
  count = fprintf(fid,format,Line_con');
  count = fprintf(fid,'   ];\n\n')

# Area data
# ----------------------------------------------------------------------
if not isempty(area),
  fm_print(['Area data are not defined in PSAT for ', ...
           'OPF computations.'])

# Supply data
# ----------------------------------------------------------------------
if not isempty(gencost)
  startup = find(gencost(:,2))
  shutdown = find(gencost(:,3))
  if startup
    fm_print(['Generation startup not supported yet. ', ...
             'Startup costs will be ignored.'])
  if shutdown
    fm_print(['Generation shutdown not supported yet. ', ...
             'Shutdown costs will be ignored.'])
  ngen = len(gen(:,1))
  ncost = len(gencost(:,1))
  coeff = np.zeros((ncost,3))
  h = find(gencost(:,1) == 1)
  if h,
    fm_print(['Piecewise linear generator costs are ', ...
             'converted in polynomial approximations.'])
for i in range(1, len(h)+1):
    n = gencost(h(i),4)
    xidx = 4+(1:2:2*n)
    yidx = 4+(2:2:2*n)
    a = polyfit(gencost(h(i),xidx),gencost(h(i),yidx),min(2,n-1))
    if len(a) == 3,
      a = a(3:-1:1)
    elseif len(a) == 2,
      a = [a(2), a(1), 0]
    else
      a = [0 1 0]
    coeff(h(i),:) = a
  h = find(gencost(:,1) == 2)
  if h  and  not isempty(find(gencost(h,4) > 3)),
    fm_print('Polynomial generator costs are reduced to 2nd order polynomials.'),
for i in range(1, len(h)+1):
    n = gencost(h(i),4)
    a = gencost(h(i),5:min(4+n,8))
    if len(a) == 3,
      a = a(3:-1:1)
    elseif len(a) == 2,
      a = [a(2), a(1), 0]
    else
      a = [0 1 0]
    coeff(h(i),:) = a
  Supply_con = np.zeros((ngen,13))
  Supply_con(:,[1 2 4 5]) = gen(:,[1 7 9 10])
  Supply_con(:,[7 8 9]) = coeff(1:ngen,:)
  if ncost == 2*ngen
    Supply_con(:,[10 11 12]) = coeff(ngen+1:ncost,:)
  Supply_con(:,13) = gen(:,8)
  count = fprintf(fid, 'Supply.con = [ ...\n')
  format = ['%4d ',repmat(' %8.4g',1,11),' %2d 0 1;\n']
  count = fprintf(fid,format,Supply_con');
  count = fprintf(fid,'   ];\n\n')

# Bus Names
# ----------------------------------------------------------------------

if isempty(bus_name)
  bus_name = cell(nbus,1)
  for i = 1:nbus,
    bus_name{i,1} = deblank(['Bus',fvar(bus(i,1),5)])

count = fprintf(fid, 'Bus.names = {...\n      ')
for i in range(1, nbus-1+1):
  count = fprintf(fid, ['''', deblank(bus_name{i}(1:min(end, 10))),'''; '])
  if rem(i,5) == 0
    count = fprintf(fid,'\n      ')
count = fprintf(fid, ['''', deblank(bus_name{end}(1:min(end, 10))),'''};\n\n'])

# end of operations
fm_print(['Conversion into data file "',pathname,newfile,'" completed.'])
if Settings.beep
  beep
fclose(fid)
check = 1
