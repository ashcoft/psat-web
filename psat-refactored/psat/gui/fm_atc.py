# Module: psat.gui.fm_atc
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_atc():

#FM_ATC determine the Available Transfer Capability (ATC)
#       by means of an iterative OPF/CPF method or a power
#       flow sensitivity analysis
#
#FM_ATC
#
#see OPF and CPF structures for settings
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

fm_var

if not autorun('ATC analysis',0)
  return

fm_disp

if not Demand.n
  fm_print('ATC computations requires the definition of "Demand" data',2)
  return
if not Supply.n
  fm_print('ATC computations requires the definition of "Supply" data',2)
  return
switch OPF.type
 case 4
  fm_print('Determination of ATC by means of an iterative OPF-CPF method')
 case 5
  fm_print('Determination of ATC by means of a power flow sensitivity analysis')
tempo1 = clock
OPF.show = 0
Settings.show = 0

# Continuation Power Flow settings
# -------------------------------------------------------------------------

CPFold = CPF
CPF.show = 0
CPF.method = 1
CPF.flow = OPF.flow
CPF.type = 3
CPF.sbus = 0
CPF.vlim = 1
CPF.ilim = 1
CPF.qlim = 1

# ===================================================================
#  Determination of "antennas", i.e. lines that connects
#  a PQ or a PV bus to the rest of the network
# ===================================================================

[busidx,lineidx] = findantennas(Line)

if ishandle(Fig.main)
  fm_disp
  if ishandle(Hdl.status)
    delete(Hdl.status)
    Hdl.status = -1
  hdl = findobj(Fig.main,'Tag','PushClose')
  set(hdl,'String','Stop')
  set(Fig.main,'UserData',1)
sp = ' * '

CPFold = CPF

# bus voltage limits
[Vmax,Vmin] = fm_vlim(1.2,0.8)

# Continuation Power Flow settings
# -----------------------------------------------------------------------

CPF.method = 1
CPF.flow = 1
CPF.type = 3
CPF.sbus = 0
CPF.vlim = 1
CPF.ilim = 1
CPF.qlim = 1
CPF.linit = 0

# =======================================================================
# First OPF solution without contingencies
# =======================================================================

fm_print('First OPF solution without faults.')
fm_opfsdr
if not OPF.conv  and  ishandle(Fig.main)
  set(Fig.main,'UserData',0)
if strcmp(History.text{end},'Optimization routine interrupted.')
  return
fm_print([sp,'ATC = ', num2str(OPF.atc)])

idx_old = 0
atc_old = 0
y_old = DAE.y
MVA = Settings.mva

[busP,idxP,idxQ] = intersect(PQ.bus,Demand.bus)
tgphi = tanphi(PQ,idxP)

# =======================================================================
#  Continuation Power Flow loop for the (N-1) contingency evaluations
# =======================================================================

while 1

  if ishandle(Fig.main)
    if not get(Fig.main,'UserData'), break, end

  lcrit = []

  Supply = pgset(Supply)
  Demand = pqset(Demand,tgphi)

#fm_disp('Continuation Power Flow Computations')

  switch OPF.type

   case 4  #  (N-1) contingency analysis

for i in range(1, Line.n+1):
      if ishandle(Fig.main)
        if not get(Fig.main,'UserData'), break, end

      fm_print('Continuation Power Flow Computations')

      if isempty(find(lineidx==i))
	fm_print(['Line #',fvar(i,4)])
	fm_print([sp,'from bus #',fvar(Line.fr(i),5), ...
		 ' to bus #',fvar(Line.to(i),5)])
	DAE.y(1:DAE.m) = OPF.yc
        len(Snapshot.y)
	DAE.x = Snapshot(1).x
	status = Line.u(i)
# set line outage
        Line = setstatus(Line,i,0)
	idx = find(abs(DAE.y(Bus.v)-Vmax) < 1e-5)
	if not isempty(idx), DAE.y(idx+Bus.n) = Vmax(idx)-1e-2; end
	CPF.init = 0
	OPF.init = 0
	a = fm_cpf('atc')
	if not isempty(a)
	  lcrit = [lcrit; [(a*totp(Demand)+totp(PQ))*MVA, i]]
	else
	  lcrit = [lcrit; [np.nan, 0]]
	fm_print([sp,'ATC = ', num2str(lcrit(end,1))])
# reset line outage
        Line.u(i) = status
# reset admittance matrix
    Line = build_y(Line)

   case 5  #  sensitivity analysis: ranking (dPij/dlambda) & (Pij)

    fm_disp
    fm_print('Sensitivity analysis.')

    lambda = OPF.guess(end-4*Bus.n)
    kg = OPF.guess(end-4*Bus.n-1-PV.n-SW.n)
    lambda = lambda - 1e-6

# active power flows in transmission lines
    [Fij,Fji] = flows(Line,'active')
    Pflow1 = max(Fij,Fji)

    PQ = pqmul(PQ,'all',1+lambda)
    pqsum(Demand,1+lambda)

    PV = pvmul(PV,'all',1+lambda+kg)
    pgsum(Supply,1+lambda+kg)

    PV = setvg(PV,'all',OPF.yc(PV.vbus))
    pg = SW.pg
    SW = setvg(SW,'all',OPF.yc(SW.vbus))
    DAE.y = OPF.yc
    fm_spf
    fm_disp

# active power flows in transmission lines
    [Fij,Fji] = flows(Line,'active')
    Pflow2 = max(Fij,Fji)

# sensitivity coefficients
    dPdl = (Pflow1-Pflow2)/1e-6
    fm_print(['Line                 |Pij(lambda)|      ', ...
	     '|Pij(lambda-dl)|   |Pij|*|d Pij/d lambda|'])
for i in range(1, Line.n+1):
      fm_print([fvar(i,4),'   ',fvar(Line.fr(i),4),'  -> ', ...
	       fvar(Line.to(i),4),' ',fvar(Pflow1(i),19), ...
	       fvar(Pflow2(i),19),fvar(Pflow1(i)*abs(dPdl(i)),19)])
    PQ = pqreset(PQ,'all')
    PV = pvreset(PV,'all')
    SW = restore(SW)
    SW = setpg(SW,'all',pg)

  fm_disp
  switch OPF.type
   case 4
    [atc,idx] = min(lcrit(:,1))
    OPF.line = lcrit(idx,2)
    fm_print(['Critical Line #',num2str(idx), ...
	     ' from bus #',fvar(Line.fr(idx),5), ...
	     ' to bus #',fvar(Line.to(idx),5)])
    fm_print([sp,'ATC = ', num2str(lcrit(idx,1))])
   case 5
    if lineidx, dPdl(lineidx) = 0; end
    pfactor = Pflow1.*abs(dPdl)
    [pfactor, pfactor_idx] = sort(pfactor)

    CPF.Pij = Pflow1
    CPF.dPdl = dPdl

    fm_print('OPF solution without contingencies:')
    fm_print([sp,'max(Pij*|dPij/dlambda)| = ', num2str(pfactor(end)), ...
	     '  (Line # ',fvar(pfactor_idx(end),4),')'])
    fm_print([sp,'lambda = ',num2str(lambda)])
    fm_print([sp,'ATC = ',num2str(OPF.atc)])
  fm_disp

#======================================================================
# OPF with inclusion of a fault on the critical line
#======================================================================

  fm_print('OPF with contingencies')

  switch OPF.type
   case 4
    CPF.init = 0
    DAE.y = Snapshot(1).y
    DAE.x = Snapshot(1).x
    fm_spf
    fm_opfsdr
    if ishandle(Fig.main)  and  not OPF.conv, set(Fig.main,'UserData',0), end
   case 5
    nopf = min(5,len(pfactor_idx))
    atc = np.zeros((nopf,1))
    rep = cell(nopf,1)
for i in range(1, nopf+1):
      OPF.init = 0
      CPF.init = 0
      if ishandle(Fig.main)
        if not get(Fig.main,'UserData'), break, end
      OPF.line = pfactor_idx(end-(i-1))
      DAE.y = Snapshot(1).y
      DAE.x = Snapshot(1).x
      fm_spf
      fm_print(['OPF computation with contingency on Line # ', ...
	       num2str(pfactor_idx(end-(i-1)))])
      fm_opfsdr
      if ishandle(Fig.main)  and  not OPF.conv, set(Fig.main,'UserData',0), end
      atc(i) = OPF.atc
      rep{i} = OPF.report
      fm_print([sp,'ATC = ', num2str(OPF.atc)])
    [atc, idx_atc] = min(atc)
    OPF.report = rep{idx_atc}
    fm_disp
    idxc = pfactor_idx(end-(idx_atc-1))
    fm_print(['Critical Line #',num2str(idxc),' from bus #', ...
	     fvar(Line.fr(idxc),5), ...
	     ' to bus #',fvar(Line.to(idxc),5)])
    fm_print([sp,'ATC = ',num2str(atc)])

# ====================================================================
#  Convergency Criteria
# ====================================================================

# stop if the method uses sensitivity analysis
  if OPF.type == 5, break, end
# stop if ATC level has not changed
  if abs(OPF.atc - atc) < 1e-2, break, end
# stop if the worst line is always the same
  if idx == idx_old(end), break, end
  idx_old = [idx_old, idx]
  if OPF.type == 4,
    if not isempty(OPF.report)
      rep_old(:,len(idx_old)-1) = OPF.report
    atc_old = [atc_old, OPF.atc]
# stop if the worst lines are always the same two
# and chose the solution which has the lowest ATC
  if len(idx_old) > 3
    if idx_old(end) == idx_old(end-2),
      fm_disp
      if atc_old(end) > atc_old(end-1),
	OPF.report = rep_old(:,end-1)
	idxc = idx_old(end-1)
      else
	idxc = idx_old(end)
      fm_print(['Critical Line #',num2str(idxc), ...
	       ' from bus #',fvar(Line.fr(idxc),5), ...
	       ' to bus #',fvar(Line.to(idxc),5)])
      break

CPF = CPFold

# restore components
Line = build_y(Line)
islands(Line)
PV = pvreset(PV,'all')
SW = restore(SW)
PQ = pqreset(PQ,'all')
Demand = restore(Demand)
Supply = restore(Supply)

if ishandle(Fig.main), set(hdl,'String','Close'); end
Settings.show = 1
OPF.show = 1
OPF.line = 0
CPF = CPFold
CPF.show = 1
CPF.init = 2
OPF.init = 0
LIB.init = 0
SNB.init = 0

if ishandle(Fig.main)
  if get(Fig.main,'UserData'),
    History.text = [History.text; ...
                    {' '; 'Final OPF Solution:'; ' '}; ...
                    OPF.report]
    fm_print(['ATC = ',num2str(atc)])
    fm_print(['ATC computation completed in ', ...
             num2str(etime(clock,tempo1)),' s'])
  else
    fm_print('ATC computation interrupted.')