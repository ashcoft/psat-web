# Module: psat.gui.fm_report
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_report():

# FM_REPORT write the power flow report.
#
# The report is saved in a text file with the same name of
# the data file followed by "_xx" where xx is a progressive
# number. Finally the report is displayed using the currently
# selected text viewer.
#
# FM_REPORT
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    23-May-2003
#Update:    24-Aug-2003
#Update:    14-Sep-2003
#Version:   2.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

fm_var

global Settings

if not Settings.init
  fm_print('Solve power flow before writing the report file')

# General variables
# --------------------------------------------------------------------

nseries = Settings.nseries
iline = [1:nseries]';
if ishandle(Fig.stat)
  hdlT = findobj(Fig.stat,'Tag','PushSort')
  string = get(hdlT,'UserData')
  switch string
   case '1n'
    [buss,ordbus] = sort(Bus.names(1:end))
    [buss,ordbus] = sort(getidx(Bus,0))
   case 'az'
    [buss,ordbus] = sort(Bus.names(1:end))
   otherwise
# nothing to do for now
else
# for command line usage, alphabetical order is used
  [buss,ordbus] = sort(Bus.names(1:end))
#[buss,ordbus] = sort(Bus.con(:,1));
nomi_bus = Bus.names
tab = '****  '
space = repmat(' ',1,11)
checkabs = Settings.absvalues
violations = Settings.violations

switch checkabs
 case 'on'
  MVA  = Settings.mva
  VB   = getkv(Bus,0,0)
  MW   = '[MW]'
  MVar = '[MVar]'
  kV   = '[kV]'
 otherwise
  MVA  = 1
  VB   = getnp.ones((Bus))
  MW   = '[p.u.]'
  MVar = '[p.u.]'
  kV   = '[p.u.]'

# check voltage and generator reactive power limits if necessary
# --------------------------------------------------------------------

if strcmp(violations,'on')

  Vbus = DAE.y(Bus.v)
  [Vmax,Vmin] = fm_vlim(1.2,0.8)
  [Qgmax,Qgmin] = fm_qlim('all')
  buses = getnp.zeros((Bus))
  buses(getbus(PV)) = 1
  buses(getbus(SW)) = 1

  vVmax = Vbus > Vmax
  vVmin = Vbus < Vmin
  vVminabs = abs(Vbus-Vmin) < Settings.lftol
  vVmaxabs = abs(Vbus-Vmax) < Settings.lftol
  vQgmax = Bus.Qg > (Qgmax+Settings.lftol)
  vQgmin = Bus.Qg < (Qgmin-Settings.lftol)
  vQgminabs = (abs(Bus.Qg-Qgmin) < Settings.lftol) & buses
  vQgmaxabs = (abs(Bus.Qg-Qgmax) < Settings.lftol) & buses
  Vmax = Vmax.*VB
  Vmin = Vmin.*VB
  Qgmax = Qgmax*MVA
  Qgmin = Qgmin*MVA


# flows in the series components
# --------------------------------------------------------------------

[P_s,Q_s,P_r,Q_r,fr_bus,to_bus] = fm_flows('bus')

line_ffr = [iline, fr_bus, to_bus, P_s*MVA, Q_s*MVA]
line_fto = [iline, to_bus, fr_bus, P_r*MVA, Q_r*MVA]

ntraf = transfno(Line) + Ltc.n + Phs.n
nline = Hvdc.n + Lines.n + Line.n - ntraf
nbranch = len(P_s)

# check transmission line limits
# --------------------------------------------------------------------

if strcmp(violations,'on')  and  Line.n
  Ss = sqrt(P_s(1:Line.n).^2+Q_s(1:Line.n).^2)
  Sr = sqrt(P_r(1:Line.n).^2+Q_r(1:Line.n).^2)
  Is = Ss./DAE.y(Line.vfr)
  Ir = Sr./DAE.y(Line.vto)
  Ps = abs(P_s(1:Line.n))
  Pr = abs(P_r(1:Line.n))
  Imax = getflowmax(Line,'imax')
  Pmax = getflowmax(Line,'pmax')
  Smax = getflowmax(Line,'smax')
  vIs = Is > Imax
  vPs = Ps > Pmax
  vSs = Ss > Smax
  vIr = Ir > Imax
  vPr = Pr > Pmax
  vSr = Sr > Smax
  Pmax = Pmax*MVA
  Smax = Smax*MVA
  Ps = Ps*MVA
  Pr = Pr*MVA
  Ss = Ss*MVA
  Sr = Sr*MVA
  Imaxs = Imax
  Imaxr = Imax
  if strcmp(checkabs,'on')
    Imaxs =1/sqrt(3)*Imax./VB(Line.fr)*MVA*1000
    Imaxr = 1/sqrt(3)*Imax./VB(Line.to)*MVA*1000
    Is =1/sqrt(3)*Is./VB(Line.fr)*MVA*1000
    Ir = 1/sqrt(3)*Ir./VB(Line.to)*MVA*1000

# Power flow report
# --------------------------------------------------------------------

fm_disp
fm_print('Writing the report file...')

# initialization of report outputs
# --------------------------------------------------------------------

Header = cell(0)
Matrix = cell(0)
Cols = cell(0)
Rows = cell(0)

# general header
# --------------------------------------------------------------------

if OPF.init
  Header{1,1}{1,1} = 'OPTIMAL POWER FLOW REPORT'
elseif CPF.init
  Header{1,1}{1,1} = 'CONTINUATION POWER FLOW REPORT'
elseif LIB.init
  Header{1,1}{1,1} = 'POWER FLOW REPORT (limit-induced bifurcation results)'
elseif SNB.init
  Header{1,1}{1,1} = 'POWER FLOW REPORT (Saddle-node bifurcation results)'
else
  Header{1,1}{1,1} = 'POWER FLOW REPORT'
Header{1,1}{2,1} = ' '
Header{1,1}{3,1} = ['P S A T  ',Settings.version]
Header{1,1}{4,1} = ' '
Header{1,1}{5,1} = 'Author:  Federico Milano, (c) 2002-2016'
Header{1,1}{6,1} = 'e-mail:  federico.milano@ucd.ie'
Header{1,1}{7,1} = 'website: faraday1.ucd.ie/psat.html'
Header{1,1}{8,1} = ' '
Header{1,1}{9,1} = ['File:  ', Path.data,strrep(File.data,'(mdl)','.mdl')]
Header{1,1}{10,1} = ['Date:  ',datestr(now,0)]

Matrix{1,1} = []
Cols{1,1} = ''
Rows{1,1} = ''

# some useful variables
# --------------------------------------------------------------------

Vs = DAE.y(ordbus+Bus.n).*VB(ordbus)
angs = DAE.y(ordbus)
raddeg = 'rad'
if ishandle(Fig.stat)
  hdlT = findobj(Fig.stat,'Tag','PushAngle')
  string = get(hdlT,'UserData')
  if not strcmp(string,'rad')
    angs = angs*180/np.pi
    raddeg = 'deg'

Pgs = Bus.Pg(ordbus)*MVA
Qgs = Bus.Qg(ordbus)*MVA
Pls = Bus.Pl(ordbus)*MVA
Qls = Bus.Ql(ordbus)*MVA

# losses
# --------------------------------------------------------------------

line_p_losses = line_ffr(:,4) + line_fto(:,4)
line_q_losses = line_ffr(:,5) + line_fto(:,5)

# network statistics
# --------------------------------------------------------------------

Header{2,1} = 'NETWORK STATISTICS'
Matrix{2,1} = Bus.n
Rows{2,1} = {'Buses:'}
Cols{2,1} = ''
if nline > 0
  Matrix{2,1}(2,1) = nline
  Rows{2,1}{2,1} = 'Lines:'
  idx = 2
else
  idx = 1
if ntraf > 0
  idx = idx + 1
  Matrix{2,1}(idx,1) = ntraf
  Rows{2,1}{idx,1} = 'Transformers:'
Matrix{2,1}(idx+1,1) = SW.n+PV.n+Syn.n
Rows{2,1}{idx+1,1} = 'Generators:'
Matrix{2,1}(idx+2,1) = PQ.n+Pl.n+Mn.n
Rows{2,1}{idx+2,1} = 'Loads:'

# statistics of the current solution algorithm
# --------------------------------------------------------------------

Header{3,1} = 'SOLUTION STATISTICS'
Cols{3,1} = ''
Rows{3,1} = {'Number of Iterations:'; ...
	     ['Maximum P mismatch ',MW]; ...
	     ['Maximum Q mismatch ',MVar]}
mp = max(abs(DAE.g(Bus.a)))
mq = max(abs(DAE.g(Bus.v)))
Matrix{3,1} = [Settings.iter; mp*MVA; mq*MVA]
if strcmp(checkabs,'off')
  Matrix{3,1}(4,1) = Settings.mva
  Rows{3,1}{4,1} = 'Power rate [MVA]'

# power flow results
# --------------------------------------------------------------------

Header{4,1} = 'POWER FLOW RESULTS'

if Settings.report #  embed line flow in bus report

  nh = 4
for i in range(1, Bus.n+1):
# bus report
    nh = nh + 1
#Header{nh,1} = nomi_bus{ordbus(i)};
    Header{nh,1} = ''
    bus_name = nomi_bus{ordbus(i)}
    Cols{nh,1} = {bus_name,'V','phase','P gen','Q gen','P load','Q load'; ...
                 ' ', kV, ['[',raddeg,']'],MW,MVar,MW,MVar}
    Rows{nh,1} = {'  '}
    Matrix{nh,1} = [Vs(i),angs(i),Pgs(i),Qgs(i),Pls(i),Qls(i)]

# violations
    if strcmp(violations,'on')
      hhh = vVmin(i) + vVmax(i) + vVmaxabs(i) + vVminabs(i) + vQgmax(i) ...
            + vQgmin(i) + vQgmaxabs(i) + vQgminabs(i)
      if hhh
        nh = nh + 1
        Header{nh} = cell(hhh,1)
      hh = 1
      if vVmin(i)
        Header{nh,1}{hh,1} = sprintf('         *  Minimum voltage limit violation [V_min = %g]',Vmin(i))
        hh = hh + 1
      if vVmax(i)
        Header{nh,1}{hh,1} = sprintf('         *  Maximum voltage limit violation [V_max = %g]',Vmax(i))
        hh = hh + 1
      if vVmaxabs(i)
        Header{nh,1}{hh,1} = sprintf('         *  Maximum voltage [V_max = %g]',Vmax(i))
        hh = hh + 1
      if vVminabs(i)
        Header{nh,1}{hh,1} = sprintf('         *  Minimum voltage [V_min = %g]',Vmin(i))
        hh = hh + 1
      if vQgmax(i)
        Header{nh,1}{hh,1} = sprintf('         *  Maximum reactive power limit violation [Qg_max = %g]',Qgmax(i))
        hh = hh + 1
      if vQgmin(i)
        Header{nh,1}{hh,1} = sprintf('         *  Minimum reactive power limit violation [Qg_min = %g]',Qgmin(i))
        hh = hh + 1
      if vQgmaxabs(i)
        Header{nh,1}{hh,1} = sprintf('         *  Maximum reactive power [Qg_max = %g]',Qgmax(i))
        hh = hh + 1
      if vQgminabs(i)
        Header{nh,1}{hh,1} = sprintf('         *  Minimum reactive power [Qg_min = %g]',Qgmin(i))

# flows
    nh = nh + 1
    Header{nh,1} = ''
    Cols{nh,1} = {'  ','To Bus','Line','P Flow', ...
                  'Q Flow','P Loss','Q Loss'; ...
                  ' ',' ',' ',MW,MVar,MW,MVar}

    idx_to = find(line_ffr(:,2) == ordbus(i))
    idx_fr = find(line_fto(:,2) == ordbus(i))
    idx_ln = [line_ffr(idx_to,3);line_fto(idx_fr,3)]
    Rows{nh,1} = cell(len(idx_ln),2)
for iii in range(1, len(idx_ln)+1):
      Rows{nh,1}{iii,1} = '  '
      Rows{nh,1}{iii,2} = nomi_bus{idx_ln(iii),1}
    Matrix{nh,1} = [[line_ffr(idx_to,1); line_fto(idx_fr,1)], ...
                    [line_ffr(idx_to,4); line_fto(idx_fr,4)], ...
                    [line_ffr(idx_to,5); line_fto(idx_fr,5)], ...
                    line_p_losses([idx_to;idx_fr]), ...
                    line_q_losses([idx_to;idx_fr])]

# check flow violations
    if strcmp(violations,'on')
      idx_ln = [line_ffr(idx_to,1);line_fto(idx_fr,1)]
for jjj in range(1, len(idx_ln)+1):
        kkk = idx_ln(jjj)
        hhh = vIs(kkk) + vPs(kkk) + vSs(kkk)
        if hhh
          nh = nh + 1
          Header{nh} = cell(hhh,1)
        hh = 1
        if vIs(kkk)
          Header{nh,1}{hh,1} = sprintf(['         *  Maximum current ', ...
                              'limit violation on line %d ', ...
                              '[I = %g > I_max = %g]'], kkk, ...
                                       Is(kkk), Imaxs(kkk))
          hh = hh + 1
        if vPs(kkk)
          Header{nh,1}{hh,1} = sprintf(['         *  Maximum real ', ...
                              'power limit violation on line %d ', ...
                              '[P = %g > P_max = %g]'], kkk, ...
                                       Ps(kkk), Pmax(kkk))
          hh = hh + 1
        if vSs(kkk)
          Header{nh,1}{hh,1} = sprintf(['         *  Maximum apparent ', ...
                              'power limit violation on line %d ', ...
                              '[S = %g > S_max = %g]'], kkk, ...
                                       Ss(kkk), Smax(kkk))

# get state and algebraic variables related to the current bus
    [x_idx,y_idx] = fm_getxy(i)
    if not isempty(x_idx)
      x_idx = sort(x_idx)
      nh = nh + 1
      Header{nh,1} = '            STATE VARIABLES'
      Rows{nh,1} = cell(len(x_idx),1)
for jhk in range(1, len(x_idx)+1):
        Rows{nh,1}{jhk,1} = ['            ',Varname.uvars{x_idx(jhk)}]
      Cols{nh,1} = ''
      Matrix{nh,1} = DAE.x(x_idx)
    if not isempty(y_idx)
      y_idx = sort(y_idx)
      nh = nh + 1
      Header{nh,1} = '            OTHER ALGEBRAIC VARIABLES'
      Rows{nh,1} = cell(len(y_idx),1)
for jhk in range(1, len(y_idx)+1):
        Rows{nh,1}{jhk,1} = ['            ',Varname.uvars{y_idx(jhk)+DAE.n}]
      Cols{nh,1} = ''
      Matrix{nh,1} = DAE.y(y_idx)


else #  classic report style

  Cols{4,1} = {'Bus','V','phase','P gen','Q gen','P load','Q load'; ...
               ' ', kV, ['[',raddeg,']'],MW,MVar,MW,MVar}
  Rows{4,1} = {nomi_bus{ordbus}}';
  Matrix{4,1} = [Vs,angs,Pgs,Qgs,Pls,Qls]
  nh = 4


# check violations
# --------------------------------------------------------------------

if strcmp(violations,'on')  and  not Settings.report
  idx = 1
  nh = nh + 1
for i in range(1, Bus.n+1):
    if vVmin(i)
      Header{nh,1}{idx,1} = sprintf('Minimum voltage limit violation at bus <%s> [V_min = %g]',Bus.names{i},Vmin(i))
      idx = idx + 1
    if vVmax(i)
      Header{nh,1}{idx,1} = sprintf('Maximum voltage limit violation at bus <%s> [V_max = %g]',Bus.names{i},Vmax(i))
      idx = idx + 1
    if vVmaxabs(i)
      Header{nh,1}{idx,1} = sprintf('Maximum voltage at bus <%s>',Bus.names{i})
      idx = idx + 1
    if vVminabs(i)
      Header{nh,1}{idx,1} = sprintf('Minimum voltage at bus <%s>',Bus.names{i})
      idx = idx + 1
    if vQgmax(i)
      Header{nh,1}{idx,1} = sprintf('Maximum reactive power limit violation at bus <%s> [Qg_max = %g]',Bus.names{i},Qgmax(i))
      idx = idx + 1
    if vQgmin(i)
      Header{nh,1}{idx,1} = sprintf('Minimum reactive power limit violation at bus <%s> [Qg_min = %g]',Bus.names{i},Qgmin(i))
      idx = idx + 1
    if vQgmaxabs(i)
      Header{nh,1}{idx,1} = sprintf('Maximum reactive power at bus <%s>',Bus.names{i})
      idx = idx + 1
    if vQgminabs(i)
      Header{nh,1}{idx,1} = sprintf('Minimum reactive power at bus <%s>',Bus.names{i})
      idx = idx + 1
  Rows{nh,1} = ''
  Cols{nh,1} = ''
  Matrix{nh,1} = []

# state variables
# --------------------------------------------------------------------

if DAE.n  and  not Settings.report
  nh = nh + 1
  Header{nh,1} = 'STATE VARIABLES'
  Rows{nh,1} = Varname.uvars([1:DAE.n])
  Cols{nh,1} = ''
  Matrix{nh,1} = DAE.x

# other algebraic variables
# --------------------------------------------------------------------

if DAE.m > 2*Bus.n  and  not Settings.report
  nh = nh + 1
  Header{nh,1} = 'OTHER ALGEBRAIC VARIABLES'
  Algnames = cell(DAE.m-2*Bus.n,1)
  idx0 = DAE.n+2*Bus.n
  for kkk = 1:(DAE.m-2*Bus.n)
    Algnames{kkk,1} = Varname.uvars{idx0+kkk}
  Rows{nh,1} = Algnames
  Cols{nh,1} = ''
  Matrix{nh,1} = DAE.y(2*Bus.n+1:DAE.m)

# line flows are printed out only for conventional reports
# --------------------------------------------------------------------

if not Settings.report

# line flows (i -> j)
  nh = nh + 1
  Header{nh,1} = 'LINE FLOWS'
  Cols{nh,1} = {'From Bus','To Bus','Line','P Flow', ...
                'Q Flow','P Loss','Q Loss'; ...
                ' ',' ',' ',MW,MVar,MW,MVar}
  Rows{nh,1} = cell(len(line_ffr(:,2)),2)
  for iii = 1:len(line_fto(:,2))
    Rows{nh,1}{iii,1} = nomi_bus{line_ffr(iii,2),1}
    Rows{nh,1}{iii,2} = nomi_bus{line_ffr(iii,3),1}
  Matrix{nh,1} = [line_ffr(:,1),line_ffr(:,4),line_ffr(:,5), ...
                  line_p_losses,line_q_losses]

# check flow violations
  if strcmp(violations,'on')
    idx = 0
    nh = nh + 1
for i in range(1, Line.n+1):
      if vIs(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            ['%sMaximum current limit violation on line %d [I = %g > I_max = ' ...
             '%g]'], space,i,Is(i),Imaxs(i))

      if vPs(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            '%sMaximum real power limit violation on line %d [P = %g > P_max = %g]', ...
            space,i,Ps(i),Pmax(i))
      if vSs(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            ['%sMaximum apparent power limit violation on line %d [S = %g > ' ...
             'S_max = %g]'], space,i,Ss(i),Smax(i))
    if idx
      Matrix{nh,1} = []
      Cols{nh,1} = ''
      Rows{nh,1} = ''
    else
      nh = nh - 1

# line flows (j -> i)
  nh = nh + 1
  Header{nh,1} = 'LINE FLOWS'
  Cols{nh,1} = {'From Bus','To Bus','Line','P Flow', ...
                'Q Flow','P Loss','Q Loss'; ...
                ' ',' ',' ',MW,MVar,MW,MVar}
  Rows{nh,1} = cell(len(line_fto(:,2)),2)
  for iii = 1:len(line_fto(:,2))
    Rows{nh,1}{iii,1} = nomi_bus{line_fto(iii,2),1}
    Rows{nh,1}{iii,2} = nomi_bus{line_fto(iii,3),1}
  Matrix{nh,1} = [line_fto(:,1),line_fto(:,4),line_fto(:,5), ...
                  line_p_losses,line_q_losses]

# check flow violations
  if strcmp(violations,'on')
    idx = 0
    nh = nh + 1
for i in range(1, Line.n+1):
      if vIr(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            ['%sMaximum current limit violation on line %d [I = %g > I_max = ' ...
             '%g]'], space,i,Ir(i),Imaxr(i))

      if vPr(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            '%sMaximum real power limit violation on line %d [P = %g > P_max = %g]', ...
            space,i,Pr(i),Pmax(i))
      if vSr(i)
        idx = idx + 1
        Header{nh,1}{idx,1} = sprintf( ...
            ['%sMaximum apparent power limit violation on line %d [S = %g > ' ...
             'S_max = %g]'], space,i,Sr(i),Smax(i))
    if idx
      Matrix{nh,1} = []
      Cols{nh,1} = ''
      Rows{nh,1} = ''
    else
      nh = nh -1

end #  end of the code for writing line flows

# global summary
# --------------------------------------------------------------------

Pg_tot = sum(Pgs)
Qg_tot = sum(Qgs)
Pl_tot = sum(Pls)
Ql_tot = sum(Qls)

total_p_loss = Pg_tot - Pl_tot
total_q_loss = Qg_tot - Ql_tot

nh = nh + 1
Header{nh,1} = 'GLOBAL SUMMARY REPORT'
Matrix{nh,1} = []
Cols{nh,1} = ''
Rows{nh,1} = ''

nh = nh + 1
Header{nh,1} = 'TOTAL GENERATION'
Matrix{nh,1} = [Pg_tot;Qg_tot]
Cols{nh,1} = ''
Rows{nh,1} = {['REAL POWER ',MW];['REACTIVE POWER ',MVar]}

nh = nh + 1
Header{nh,1} = 'TOTAL LOAD'
Matrix{nh,1} = [Pl_tot;Ql_tot]
Cols{nh,1} = ''
Rows{nh,1} = {['REAL POWER ',MW];['REACTIVE POWER ',MVar]}

nh = nh + 1
Header{nh,1} = 'TOTAL LOSSES'
Matrix{nh,1} = [total_p_loss;total_q_loss]
Cols{nh,1} = ''
Rows{nh,1} = {['REAL POWER ',MW];['REACTIVE POWER ',MVar]}

# violation summary
# --------------------------------------------------------------------

if strcmp(violations,'on')
  nh = nh + 1
  Header{nh,1}{1,1} = 'LIMIT VIOLATION STATISTICS'
  vVtot = sum(vVmax)+sum(vVmin)
  vQtot = sum(vQgmax)+sum(vQgmin)
  vVabs = sum(vVmaxabs)+sum(vVminabs)
  vQabs = sum(vQgmaxabs)+sum(vQgminabs)
  if vVtot
    Header{nh,1}{2,1} = sprintf('# OF VOLTAGE LIMIT VIOLATIONS: %d',vVtot)
  else
    if vVabs
      Header{nh,1}{2,1} = sprintf(['ALL VOLTAGES WITHIN LIMITS (%d ' ...
                          'BINDING).'],vVabs)
    else
      Header{nh,1}{2,1} = 'ALL VOLTAGES WITHIN LIMITS.'
  if vQtot
    Header{nh,1}{3,1} = sprintf('# OF REACTIVE POWER LIMIT VIOLATIONS: %d',vQtot)
  else
    if vQabs
      Header{nh,1}{3,1} = sprintf(['ALL REACTIVE POWERS WITHIN LIMITS (%d ' ...
                          'BINDING).'],vQabs)
    else
      Header{nh,1}{3,1} = 'ALL REACTIVE POWER WITHIN LIMITS.'
  if Line.n
    vItot = sum(vIs & vIr)
    if vItot
      Header{nh,1}{4,1} = sprintf('# OF CURRENT FLOW LIMIT VIOLATIONS: %d',vItot)
    else
      Header{nh,1}{4,1} = 'ALL CURRENT FLOWS WITHIN LIMITS.'
    vPtot = sum(vPs & vPr)
    if vPtot
      Header{nh,1}{5,1} = sprintf('# OF ACTIVE POWER FLOW LIMIT VIOLATIONS: %d',vPtot)
    else
      Header{nh,1}{5,1} = 'ALL REAL POWER FLOWS WITHIN LIMITS.'
    vStot = sum(vSs & vSr)
    if vStot
      Header{nh,1}{6,1} = sprintf('# OF APPARENT POWER FLOW LIMIT VIOLATIONS: %d',vStot)
    else
      Header{nh,1}{6,1} = 'ALL APPARENT POWER FLOWS WITHIN LIMITS.'
  Matrix{nh,1} = []
  Cols{nh,1} = ''
  Rows{nh,1} = ''

# writing data...
# --------------------------------------------------------------------

fm_write(Matrix,Header,Cols,Rows)