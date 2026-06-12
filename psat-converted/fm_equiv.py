# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_equiv.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function check = fm_equiv
# FM_EQUIV computes simple static and dynamic network equivalents
#
#see also the function FM_EQUIVFIG
#
#Author:    Federico Milano
#Update:    02-Apr-2008
#Version:   0.1
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano


global EQUIV Settings Path File DAE Bus
global Line PQ Shunt PV SW Syn Exc Pl Mn

check = 0

if not autorun('Network Equivalent',1)
  return

fm_print(' ')

switch EQUIV.equivalent_method
 case 1
  fm_print('Equivalencing procedure. Thevenin equivalents.')
 case 2
  fm_print('Equivalencing procedure. Dynamic equivalents.')
 otherwise
  fm_print('Error: Unknown equivalencing procedure.',2)
  return

# define the bus list
write_buslist
if isempty(EQUIV.buslist)
  fm_print('Error: There were problems in writing the bus list selection.',2)
  return

if EQUIV.island  and  EQUIV.stop_island
  fm_print('Error: The equivalent procedure cannot continue',2)
  return

# check equivalent method consistency
#if ~DAE.n  and  EQUIV.equivalent_method == 2
#  fm_disp('The network does not contain dynamic data.')
#  fm_disp('Thevenin equivalent method will be used.')
#  EQUIV.equivalent_method = 1;
#end

# open data file for the equivalent network
cd(Path.data)
jobname = strrep(File.data,'(mdl)','')
fid = fopen([jobname,'_equiv.m'],'wt')

# headers
fprintf(fid,['%% ',jobname,' (Equivalent network created by EQUIV)\n'])
fprintf(fid,'%%\n\n')

# restore static data that can have been modified during power flow.
SW = restore(SW)
PV = restore(PV)
PQ = restore(PQ)
Pl = restore(Pl)
Mn = restore(Mn)
Settings.init = 0

# write data
write(Bus,fid,EQUIV.buslist)
write(Line,fid,EQUIV.buslist)
write(PQ,fid,EQUIV.buslist,'PQ')
write(Pl,fid,EQUIV.buslist)
write(Mn,fid,EQUIV.buslist)
write(Shunt,fid,EQUIV.buslist)
slack = write(SW,fid,EQUIV.buslist)
slack = write(PV,fid,EQUIV.buslist,slack)
[borderbus,gengroups,yi,y0,zth] = equiv(Line,fid)
synidx = write(Syn,fid,EQUIV.buslist)
write(Exc,fid,synidx,0)

xbus = borderbus + Bus.n
nborder = len(borderbus)

# write external buses
Buseq = BUclass
Buseq.con = Bus.con(borderbus,:)
Buseq.con(:,1) = xbus
Buseq.names = fm_strjoin('X',Bus.names(borderbus))
write(Buseq,fid,1:len(Buseq.names))

[idx1,idx2,busidx1,busidx2] = filter(Line,EQUIV.buslist)

beq = np.zeros((len(EQUIV.buslist),1))
peq = beq
qeq = beq

for i in range(1, len(busidx1)+1):
  [Pij,Qij,Pji,Qji] = flows(Line,'pq',idx1{i})
  h = busidx1(i)
  beq(h) = EQUIV.buslist(h)
  peq(h) = -sum(Pij)
  qeq(h) = -sum(Qij)

for i in range(1, len(busidx2)+1):
  [Pij,Qij,Pji,Qji] = flows(Line,'pq',idx2{i})
  h = busidx2(i)
  beq(h) = EQUIV.buslist(h)
  peq(h) = peq(h)-sum(Pji)
  qeq(h) = qeq(h)-sum(Qji)

ieq = find(beq)
beq = beq(ieq)
peq = peq(ieq)
qeq = qeq(ieq)
zth = zth(ieq)

# take into account that the REI equivalent add a shunt load at the border
if EQUIV.equivalent_method == 2
  vbd = DAE.y(borderbus + Bus.n)
  vb2 = vbd.*vbd
  peq = peq-real(y0).*vb2
# qeq = qeq-imag(y0).*vb2;

# compute and write synchronous machine equivalents
if EQUIV.equivalent_method == 2  and  Syn.n
  Syneq = SYclass
  [Syneq.con,pf] = equiv(Syn,borderbus,gengroups,yi)
# discard generators that are producing negative active power
  gdx = find(peq > 1e-3)
  if not isempty(gdx)
# synchronous machines
    bdx = find(ismember(Syneq.con(:,1),beq(gdx)+Bus.n))
    Syneq.con = Syneq.con(bdx,:)
    Syneq.bus = Syneq.con(:,1)
    nsyn = len(Syneq.bus)
    Syneq.u = np.ones((nsyn,1))
    Syneq.n = nsyn
    write(Syneq,fid,xbus)
# automatic voltage regulators
    AVReq = AVclass
    AVReq.con = equiv(Exc,gengroups(gdx),pf(bdx),len(synidx))
    AVReq.syn = AVReq.con(:,1)
    AVReq.n = len(AVReq.syn)
    AVReq.u = np.ones((AVReq.n,1))
    write(AVReq,fid,AVReq.syn,len(synidx))

# write slack bus data if needed
if not slack
  [pmax,h] = max(abs(peq))
  [v,a,p] = veq(zth(h),peq(h),qeq(h),beq(h))
  data = [beq(h)+Bus.n,Settings.mva,getkv(Bus,beq(h),1),v,a,0,0,1.1,0.9,p,1,1,1]
  SWeq = SWclass
  SWeq.con = data
  SWeq.bus = beq(h)+Bus.n
  SWeq.n = 1
  SWeq.u = 1
  slack = write(SWeq,fid,beq(h)+Bus.n)
  beq(h) = []
  peq(h) = []
  qeq(h) = []

# write equivalent PV or PQ generators at external buses
xbeq = beq+Bus.n
switch EQUIV.gentype
 case 1
  data = np.zeros((len(beq),11))
for h in range(1, len(beq)+1):
    [v,a,p,q] = veq(zth(h),peq(h),qeq(h),beq(h))
    data(h,:) = [xbeq(h),Settings.mva,getkv(Bus,beq(h),1),p,v,0,0,1.1,0.9,1,1]
  PVeq = PVclass
  PVeq.con = data
  PVeq.bus = xbeq
  PVeq.n = len(beq)
  PVeq.u = np.ones((len(beq),1))
  write(PVeq,fid,xbeq,slack)
 case 2
  data = np.zeros((len(beq),9))
  pdx = []
for h in range(1, len(beq)+1):
    [v,a,p,q] = veq(zth(h),peq(h),qeq(h),beq(h))
    data(h,:) = [xbeq(h),Settings.mva,getkv(Bus,beq(h),1),p,q,1.1,0.9,1,1]
    if abs(p) < 1e-3  and  abs(q) < 1e-3
      pdx = [pdx; h]
  PQeq = PQclass
  if not isempty(pdx)
    data(pdx,:) = []
    xbeq(pdx) = []
  PQeq.con = data
  PQeq.bus = xbeq
  PQeq.n = len(xbeq)
  PQeq.u = np.ones((len(xbeq),1))
  write(PQeq,fid,xbeq,'PQgen')

# close file
fclose(fid)
cd(Path.local)

# everything ok
check = 1

# -------------------------------------------------------------------------
# This function returns the indexes of the current bus list
# -------------------------------------------------------------------------
def write_buslist():

global EQUIV Line Bus Path File

EQUIV.buslist = []

switch EQUIV.bus_selection

 case 1 #  voltage level

  buslist = find(getkv(Bus,0,0) == EQUIV.bus_voltage)
  if isempty(buslist)
    print(['There is no bus whose nominal voltage is ', ...
          num2str(EQUIV.bus_voltage)])
    return

 case 2 #  area

  buslist = find(getarea(Bus,0,0) == EQUIV.area_num)
  if isempty(buslist)
    print(['There is no bus whose nominal voltage is >= ', ...
          num2str(EQUIV.bus_voltage)])
    return

 case 3 #  region

  buslist = find(getregion(Bus,0,0) == EQUIV.region_num)
  if isempty(buslist)
    print(['There is no bus whose nominal voltage is >= ', ...
          num2str(EQUIV.bus_voltage)])
    return

 case 4 #  voltage threshold

  buslist = find(getkv(Bus,0,0) >= EQUIV.bus_voltage)
  if isempty(buslist)
    print(['There is no bus whose nominal voltage is >= ', ...
          num2str(EQUIV.bus_voltage)])
    return

 case 5 #  custom bus list

  if isempty(EQUIV.custom_file)
    print('Warning: No bus list file selected!')
  [fid,msg] = fopen([EQUIV.custom_path,EQUIV.custom_file],'rt')
  if fid == -1
    print(msg)
    print('An empty bus list is returned.')
    return
# scanning bus list file
  buslist = []
  while not feof(fid)
    busname = deblank(fgetl(fid))
    buslist = [buslist; strmatch(busname,Bus.names,'exact')]
  if isempty(buslist)
    print('There is no bus whose name matches the given bus list.')
    return

 otherwise

  print('Unkonwn bus selection type.  Empty bus list is returned.')


# removing repetitions
buslist = unique(buslist)

# bus depth
nd = EQUIV.bus_depth

# line indexes
busfr = Line.fr
busto = Line.to
idxLd = [busfr; busto]
idxLq = [busto; busfr]

# bus search
newbus = []
for i in range(1, len(buslist)+1):
  busi = buslist(i)
  newbus = [newbus; searchbus(nd,busi,idxLd,idxLq)]

# removing repetions again
if not isempty(newbus)
  buslist = unique([buslist; newbus])

# check equivalent network connectivity
Bn = len(buslist)
Busint(buslist,1) = [1:Bn]
busmax = len(Busint)
idxL = find(ismember(busfr,buslist).*ismember(busto,buslist))
Lfr = Busint(busfr(idxL))
Lto = Busint(busto(idxL))
u = Line.u(idxL)

# connectivity matrix
connect_mat = ...
    sparse(Lfr,Lfr,1,Bn,Bn) + ...
    sparse(Lfr,Lto,u,Bn,Bn) + ...
    sparse(Lto,Lto,u,Bn,Bn) + ...
    sparse(Lto,Lfr,1,Bn,Bn)
# find network islands using QR factorization
[Q,R] = qr(connect_mat)
idx = find(abs(sum(R,2)-diag(R)) < 1e-5)
nisland = len(idx)
if nisland > 1
  print(['There are ',num2str(nisland),' islanded networks.'])
  EQUIV.island = nisland
else
  print(['The equivalent network is interconnected.'])

EQUIV.buslist = buslist

# -------------------------------------------------------------------------
# recursive bus search up to the desired depth
# -------------------------------------------------------------------------
function newbus = searchbus(nd,busi,idxLd,idxLq)

newbus = []
if not nd, return, end
idx = find(idxLd == busi)
if not isempty(idx)
  newbus = idxLq(idx)
for i in range(1, len(newbus)+1):
    newbus = [newbus; searchbus(nd-1,newbus(i),idxLd,idxLq)]

# -------------------------------------------------------------------------
# compute the voltage and power at the recieving end of external lines
# -------------------------------------------------------------------------
function [v,a,p,q] = veq(zth,peq,qeq,idx)

global DAE Bus

if isempty(zth), return, end

v1 = DAE.y(Bus.n+idx)*exp(i*DAE.y(idx))
i21 = (peq-i*qeq)/conj(v1)
v2 = v1 + zth*i21
s = v2*conj(i21)
p = real(s)
q = imag(s)
v = abs(v2)
a = angle(v2)