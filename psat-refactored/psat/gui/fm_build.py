# Module: psat.gui.fm_build
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_build():

#FM_BUILD build new component functions (Symbolic Toolbox is needed)
#
#FM_BUILD
#
#see also FM_MAKE FM_COMPONENT
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    19-Dec-2003
#Version:   1.0.1
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Comp Settings Fig Path
global Algeb Buses Initl Param Servc State

# ***********************************************************************
# some control variables
error_v = []
lasterr('')
null = '0'

# useful strings
c_name = Comp.name
c_name(1) = upper(c_name(1))

# variable arrays
state_vect = varvect(State.name, ' ')
algeb_vect = varvect(Algeb.name, ' ')
param_vect = varvect(Param.name, ' ')
initl_vect = varvect(Initl.name, ' ')
servc_vect = varvect(Servc.name, ' ')
pq_Servc = 0

# equation arrays
servc_eq = varvect(Servc.eq,'; ')
state_eq = varvect(State.eq,'; ')
algeb_eq = varvect(Algeb.eq,'; ')

# ********************************************************************************
# check equations
if State.neq > 0
  state_check = strmatch('null',State.eq,'exact')
  if state_check
    error_v = [error_v; ...
               fm_strjoin('Differential equation for "', ...
                      State.eqidx(state_check), ...
                      '" has not been defined.')]
if Servc.neq > 0
  servc_foo = fm_strjoin(Servc.type,Servc.eq)
  servc_check = strmatch('Innernull',servc_foo,'exact')
  servc_check = [servc_check; strmatch('Outputnull',servc_foo,'exact')]
  if servc_check
    error_v = [error_v; ...
               fm_strjoin('Service equation for "', ...
                      Servc.eqidx(servc_check), ...
                      '" has not been defined.')]

# ********************************************************************************
# check variable usage
servc_idx = [strmatch('Inner',Servc.type); strmatch('Output',Servc.type)]
total_var = [State.name; Algeb.name; Servc.eqidx(servc_idx); Param.name; Initl.name]
total_eqn = [' ',servc_eq,' ',state_eq,' ',algeb_eq,' ',varvect(State.time,'*'),' ']
for i in range(1, len(total_var)+1):
  idx = findstr(total_eqn,total_var{i})
  if isempty(idx)
    error_v{end+1,1} = ['The variable "',total_var{i},'" is not used in any equation.']
  else
    before = total_eqn(idx-1)
    after  = total_eqn(idx+len(total_var{i}))
    check = 1
for j in range(1, len(idx)+1):
      a = double(after(j));       b = double(before(j))
      a1 = not isletter(after(j));   a2 = (a != 95);  a3 = (a > 57  or  a < 48)
      b1 = not isletter(before(j));  b2 = (b != 95);  b3 = (b > 57  or  b < 48)
      if a1  and  a2  and  a3  and  b1  and  b2  and  b3, check = 0; break, end
    if check
      error_v{end+1,1} = ['The variable "',total_var{i}, ...
                          '" is not used in any equation.']

# ********************************************************************************
# symbolic variables
try
  if state_vect, eval(['syms ',state_vect]), end
  if algeb_vect, eval(['syms ',algeb_vect]), end
  if param_vect, eval(['syms ',param_vect]), end
  if servc_vect, eval(['syms ',servc_vect]), end
  if initl_vect, eval(['syms ',initl_vect]), end

# compute Jacobians matrices (Maple Symbolic Toolbox)
  if not isempty(state_eq)
    if not isempty(state_vect)
      eval(['Fx = jacobian([',state_eq, '],[', state_vect, ']);'])
    if not isempty(algeb_vect)
      eval(['Fy = jacobian([',state_eq, '],[', algeb_vect, ']);'])
    if not isempty(servc_vect)
      eval(['Fz = jacobian([',state_eq, '],[', servc_vect, ']);'])
    if pq_Servc
      eval(['Fpq = jacobian([',state_eq, '],[', pq_vect, ']);'])
  if not isempty(algeb_eq)
    if not isempty(state_vect)
      eval(['Gx = jacobian([',algeb_eq, '],[', state_vect, ']);'])
    if not isempty(algeb_vect)
      eval(['Gy = jacobian([',algeb_eq, '],[', algeb_vect, ']);'])
    if not isempty(servc_vect)
      eval(['Gz = jacobian([',algeb_eq, '],[', servc_vect, ']);'])
    if pq_Servc
      eval(['Gpq = jacobian([',alg_eqeb, '],[', pq_vect, ']);'])
  if not isempty(servc_eq)
    if not isempty(state_vect)
      eval(['Zx = jacobian([',servc_eq, '],[', state_vect, ']);'])
    if not isempty(algeb_vect)
      eval(['Zy = jacobian([',servc_eq, '],[', algeb_vect, ']);'])
    if not isempty(servc_vect)
      eval(['Zz = jacobian([',servc_eq, '],[', servc_vect, ']);'])
    if pq_Servc
      eval(['Zpq = jacobian([',servc_eq, '],[', pq_vect, ']);'])

# ********************************************************************************
# check synthax of equations
for i in range(1, State.neq+1):
  try
    eval([State.eq{i,1},';'])
  catch
    error_v{end+1,1} = [lasterr, ' (In differential equation "', ...
                        State.eq{i,1}, '")']
  try
    eval([State.init{i,1},';'])
  catch
    error_v{end+1,1} = [lasterr, ' (In state variable  "', ...
                        State.name{i,1}, '" initialization expression)']
  state_init{i,1} = vectorize(State.init{i,1})
for i in range(1, Algeb.neq+1):
  try
    eval([Algeb.eq{i,1},';'])
  catch
    error_v{end+1,1} = [lasterr, ' (In algebraic equation "', ...
                        State.eq{i,1}, '")']
for j in range(1, Servc.neq+1):
  try
    eval([Servc.eq{i,1},';'])
  catch
    error_v{end+1,1} = [lasterr, ' (In service equation "', ...
                        Servc.eqidx{i,1}, '")']

# check component name
if isempty(Comp.name)
  error_v{end+1,1} = 'Component name is empty.'
  return

# ********************************************************************************
# display errors
if not isempty(error_v)
  error_v = fm_strjoin('Error#',num2str([1:len(error_v)]'),': ',error_v);
  error_v = [{['REPORT OF ERRORS ENCOUNTERED WHILE BUILDING ', ...
               'NEW COMPONENT "',Comp.name,'.m"']}; error_v]
  error_v{end+1,1} = ['BUILDING NEW COMPONENT FILE "', ...
                      Comp.name,'.m" FAILED']
  fm_disp
  fm_print(error_v{1:end-1})
  fm_print(['BUILDING NEW COMPONENT FILE "',Comp.name,'.m" FAILED'])

  fm_update
  set(findobj(Fig.update,'Tag','Listbox1'),'String',error_v, ...
                    'BackgroundColor','w', ...
                    'ForegroundColor','r', ...
                    'Enable','inactive', ...
                    'max',2, ...
                    'Value',[])
  set(findobj(Fig.update,'Tag','Pushbutton2'),'Enable','off')
  return

# ***********************************************************************
# check for previous versions
a = what(Path.psat)
olderfile = strmatch(['fm_',Comp.name,'.m'],a.m,'exact')
if not isempty(olderfile)
  uiwait(fm_choice(['Overwrite Existing File "fm_',Comp.name,'.m" ?']))
  if not Settings.ok, return, end

# ***********************************************************************
# open new component file
fid = fopen([Path.psat, 'fm_', Comp.name,'.m'], 'wt')
if fid == -1
  fm_print(['Cannot open file fm_',Comp.name,'. Check permissions'])
  return
fprintf(fid, ['function  fm_', Comp.name, '(flag)'])

# write help of the function
if isempty(Comp.descr)
  Comp.descr = ['Algebraic Differential Equation ', ...
                Comp.name, '.m']
fprintf(fid, ['\n\n%%FM_', upper(Comp.name),' defines ',Comp.descr])

# ********************************************************************
# data format .con
fprintf(fid, ['\n%%\n%%Data Format ', c_name, '.con:'])
fprintf(fid, '\n%%  col #%d: Bus %d number',[1:Buses.n;1:Buses.n])
idx_inn = strmatch('Inner',  Servc.type, 'exact')
idx_inp = strmatch('Input',  Servc.type, 'exact')
idx_out = strmatch('Output', Servc.type, 'exact')

fprintf(fid, '\n%%  col #%d: Power rate [MVA]',Buses.n+1)
fprintf(fid, '\n%%  col #%d: Bus %d Voltage Rate [kV]', ...
        [Buses.n+1+[1:Buses.n];1:Buses.n])
fprintf(fid, '\n%%  col #%d: Frequency rate [Hz]',2*Buses.n+2)
inip = 2*Buses.n+3
endp  = 2*Buses.n+2+Param.n
pidx = inip:endp
for i in range(1, len(pidx)+1):
  fprintf(fid, '\n%%  col #%d: %s %s [%s]', ...
          pidx(i),Param.name{i},Param.descr{i},Param.unit{i})

x_max = [1:State.n]
if State.n
  x_idx = strmatch('None',State.limit(:,1),'exact')
  x_max(x_idx) = []
x_min = [1:State.n]
if State.n
  x_idx = strmatch('None',State.limit(:,2),'exact')
  x_min(x_idx) = []
n_xmax = len(x_max); n_xmin = len(x_min)
for i in range(1, n_xmax+1):
  fprintf(fid,'\n%%  col #%d: %s',endp+i, ...
          State.limit{x_max(i),1})
for i in range(1, n_xmin+1):
  fprintf(fid,'\n%%  col #%d: %s',endp+n_xmax+i, ...
          State.limit{x_min(i),1})

s_max = [1:Servc.neq]
if Servc.n
  s_idx = strmatch('None',Servc.limit(:,1),'exact')
  s_max(s_idx) = []
s_min = [1:Servc.neq]
if Servc.n
  s_idx = strmatch('None',Servc.limit(:,2),'exact')
  s_min(s_idx) = []
n_smax = len(s_max); n_smin = len(s_min)
for i in range(1, n_smax+1):
  fprintf(fid,'\n%%  col #%d: %s', ...
          endp+n_xmax+n_xmin+i,Servc.limit{s_max(i),1})
for i in range(1, n_smin+1):
  fprintf(fid,'\n%%  col #%d: %s', ...
          endp+n_xmax+n_xmin+n_smax+i,Servc.limit{s_min(i),1})

okdata = 0
nidx = 0
if not isempty(idx_inn)  or  not isempty(idx_out)
  okdata = 1
if Initl.n  or  okdata
  fprintf(fid, ['\n%% \n%%Data Structure: ', c_name, '.dat:'])
for i in range(1, Initl.n+1):
  fprintf(fid,'\n%%  col #%d: %s', i,Initl.name{i})
if okdata
  nidx = len(idx_inn)+len(idx_out)
  iidx = [idx_inn;idx_out]
for i in range(1, nidx+1):
    fprintf(fid,'\n%%  col #%d: %s', ...
            Initl.n+i,Servc.eqidx{iidx(i)})

# function calls
fprintf(fid, ['\n%% \n%%FM_', upper(Comp.name),'(FLAG)'])
if Comp.init
  fprintf(fid, ['\n%%   FLAG = 0 -> initialization'])
if not isempty(algeb_eq)
  fprintf(fid, ['\n%%   FLAG = 1 -> algebraic equations'])
  fprintf(fid, ['\n%%   FLAG = 2 -> algebraic Jacobians'])
if not isempty(state_eq)
  fprintf(fid, ['\n%%   FLAG = 3 -> differential equations'])
  fprintf(fid, ['\n%%   FLAG = 4 -> state Jacobians'])
if n_xmax  or  n_xmin > 0
  fprintf(fid, ['\n%%   FLAG = 5 -> non-windup limiters)'])
fprintf(fid, '\n%% \n%%Author:    File automatically generated by PSAT')
fprintf(fid, '\n%%Date:      %s',date)

# global variables
fprintf(fid, ['\n\nglobal ',c_name,' DAE Bus Settings'])

# ************************************************************************
# general settings
fprintf(fid, '\n')
for i in range(1, State.n+1):
  fprintf(fid,'\n%s = DAE.x(%s.%s);',State.name{i},c_name, ...
          State.name{i})
if Algeb.n
  idx_v = strmatch('V',Algeb.name)
  idx_a = strmatch('t',Algeb.name)
  if idx_v
    num_v = strrep(Algeb.name(idx_v),'V','')
    if Buses.n == 1
      fprintf(fid,'\n%s = DAE.y(%s.bus+Bus.n);', ...
              Algeb.name{idx_v},c_name)
    else
for i in range(1, len(idx_v)+1):
        fprintf(fid,'\n%s = DAE.y(%s.bus%s+Bus.n);', ...
                Algeb.name{idx_v(i)},c_name,num_v{i})
  if idx_a
    num_a = strrep(Algeb.name(idx_a),'theta','')
    if Buses.n == 1
      fprintf(fid,'\n%s = DAE.y(%s.bus);', ...
              Algeb.name{idx_a},c_name)
    else
for i in range(1, len(idx_a)+1):
        fprintf(fid,'\n%s = DAE.y(%s.bus%s);', ...
                Algeb.name{idx_a(i)},c_name,num_a{i})
for i in range(1, Param.n+1):
  fprintf(fid,'\n%s = %s.con(:,%d);',Param.name{i},c_name,pidx(i))
for i=1:n_xmax,
  fprintf(fid,'\n%s = %s.con(:,%d);',State.limit{x_max(i),1}, ...
	  c_name,endp+i)
for i=1:n_xmin,
  fprintf(fid,'\n%s = %s.con(:,%d);',State.limit{x_min(i),2}, ...
	  c_name,endp+n_xmax+i)
for i=1:n_smax,
  fprintf(fid,'\n%s = %s.con(:,%d);',Servc.limit{s_max(i),1}, ...
	  c_name,endp+n_xmax+n_xmin+i)
for i=1:n_smin,
  fprintf(fid,'\n%s = %s.con(:,%d);',Servc.limit{s_min(i),2}, ...
	  c_name,endp+n_xmax+n_xmin+n_smax+i)
for i=1:Initl.n,
  fprintf(fid,'\n%s = %s.dat(:,%d);',Initl.name{i},c_name,i)
for i=1:nidx,
  fprintf(fid,'\n%s = %s.dat(:,%d);',Servc.eqidx{iidx(i)},c_name, ...
	  Initl.n+i)

# **********************************************************************
# initialization
if Comp.init
  fprintf(fid, '\n\nswitch flag\n case 0 %% initialization')
  msg = ['Component']
  idx_T = [1:State.n]
  idx = strmatch('None',State.time,'exact')
  idx_T(idx) = []
  if idx_T
    fprintf(fid,'\n\n  %%check time constants')
  for i=1:len(idx_T),
    fprintf(fid,['\n  idx = find(%s == 0);\n  if idx\n    ', ...
                 Comp.name,'warn(idx, ''Time constant %s ', ...
                 'cannot be zero. %s = 0.001 s will be used.''),\n  ' ...
                 'end'],State.time{idx_T(i)}, ...
                 State.time{idx_T(i)},State.time{idx_T(i)})
    fprintf(fid,'\n  %s.con(idx,%d) = 0.001;', ...
            c_name,pidx(strmatch(State.time{idx_T(i)}, ...
                                 Param.name,'exact')))
  fprintf(fid,'\n\n  %%variable initialization')
  for i=1:State.n,
    fprintf(fid,'\n  DAE.x(%s.%s) = %s;',c_name,State.name{i},state_init{i})
    fprintf(fid,'\n  %s = DAE.x(%s.%s);',State.name{i},c_name,State.name{i})
  for i=1:nidx,
    fprintf(fid,'\n  %s.dat(:,%d) = %s;',Initl.n+i,c_name,vectorize(Servc.eq{i}))
    fprintf(fid,'\n  %s = %s.dat(:,%d);',Servc.eqidx{iidx(i)},c_name,Initl.n+i)
for i in range(1, Initl.n+1):
    fprintf(fid,'\n  %s.dat(:,%d) = %s;',c_name,i, ...
            strrep(Initl.name{i},'_0',''))
  fprintf(fid,'\n\n  %%check limits')
for i in range(1, n_xmax+1):
    fprintf(fid,['\n  idx = find(%s > %s_max); if idx, ', ...
                 Comp.name,'warn(idx, '' State variable %s ', ...
                 'is over its maximum limit.''), end'], ...
            State.name{x_max(i)},State.name{x_max(i)}, ...
            State.name{x_max(i)})
for i in range(1, n_xmin+1):
    fprintf(fid,['\n  idx = find(%s < %s_min); if idx, ', ...
                 Comp.name,'warn(idx, '' State variable %s ', ...
                 'is under its minimum limit.''), end'], ...
            State.name{x_min(i)},State.name{x_min(i)}, ...
            State.name{x_min(i)})
for i in range(1, n_smax+1):
    fprintf(fid,['\n  idx = find(%s > %s_max); if idx, ', ...
                 Comp.name,'warn(idx, '' State variable %s ', ...
                 'is over its maximum limit.''), end'], ...
            Servc.name{s_max(i)},Servc.name{s_max(i)}, ...
            Servc.name{s_max(i)})
for i in range(1, n_smin+1):
    fprintf(fid,['\n  idx = find(%s < %s_min); if idx, ', ...
                 Comp.name,'warn(idx, '' State variable %s ', ...
                 'is under its minimum limit.''), end'], ...
            Servc.name{s_min(i)},Servc.name{s_min(i)}, ...
            Servc.name{s_min(i)})
  fprintf(fid,['\n  fm_disp(''Initialization of ',c_name, ...
               'components completed.'')\n'])

# **********************************************************************
# algebraic equations
if not isempty(algeb_eq)
  if Comp.init
    fprintf(fid, '\n case 1 %% algebraic equations\n')
  else
    fprintf(fid, '\n\nswitch flag\n case 1 %% algebraic equations\n')

aidx = [1:Algeb.neq]
idx = strmatch('null',Algeb.eq)
aidx(idx) = []
idx = strmatch('0',Algeb.eq)
aidx(idx) = []
for i in range(1, len(aidx)+1):
  if Buses.n == 1
    a1 = ''
  else
    a1 = num2str(ceil(aidx(i)/2))
  if rem(aidx(i),2)
    fprintf(fid,'\n  DAE.g = DAE.g + sparse(%s.bus%s,1,%s,DAE.m,1);', ...
            c_name,a1,vectorize(Algeb.eq{aidx(i)}))
  else
    fprintf(fid,'\n  DAE.g = DAE.g + sparse(%s.bus%s+Bus.n,1,%s,DAE.m,1);', ...
            c_name,a1,vectorize(Algeb.eq{aidx(i)}))

# ********************************************************************
# algebraic Jacobians

# substitution of inner service variables
for j in range(1, 5+1):
for i in range(1, Servc.neq+1):
    if strcmp(Servc.type{i},'Inner')  and  not strcmp(Servc.eq{i},'null')
      state_eq = strrep(state_eq,Servc.eqidx{i},['(',Servc.eq{i},')'])
      algeb_eq = strrep(algeb_eq,Servc.eqidx{i},['(',Servc.eq{i},')'])
      servc_eq = strrep(servc_eq,Servc.eqidx{i},['(',Servc.eq{i},')'])

if not isempty(algeb_eq)
  fprintf(fid, '\n\n case 2 %% algebraic Jacobians\n')
eqformat = '\n  DAE.J%d%d = DAE.J%d%d + sparse(%s.bus%s,%s.bus%s,%s,Bus.n,Bus.n);'

for j in range(1, len(aidx)+1):
  i = aidx(j)
  a1 = 2-rem(i,2)
  if Buses.n == 1
    a2 = ''
  else
    a2 = num2str(ceil(i/2))
for h in range(1, Algeb.n+1):
    type = Algeb.name{h,1}
    if strcmp(type(1), 'V')
      a3 = 2
      if Buses.n == 1
        a4 = ''
      else
        a4 = type(2:len(type))
    elseif strcmp(type(1:5), 'theta')
      a3 = 1
      if Buses.n == 1
        a4 = ''
      else
        a4 = type(6:len(type))
    if not strcmp(char(Gy(i,h)),'0')
      fprintf(fid,eqformat,a1,a3,a1,a3,c_name,a2,c_name,a4, ...
              vectorize(char(Gy(i,h))))

# check limits in case of state variable dependancies
Temp = 0
for i = 1:Servc.neq; Temp = not strcmp(Servc.limit{i},'None'); break; end
S = 0
if Temp
  for i = 1:Servc.neq; S = not strcmp(Servc.type{i},'Input'); break; end
if S
  fprintf(fid,'\n')
for i in range(1, len(Servc.eqidx)+1):
    s_var = Servc.eqidx{i}
    for k = 1:Servc.neq; if strcmp(s_var,Servc.name{k}); break; end; end
    if not strcmp(Servc.type{k},'Input')  and  not isempty(findstr(algeb_eq,s_var))
      a = strcmp(Servc.limit{k,1},'None')
      b = strcmp(Servc.limit{k,2},'None')
      if not a  or  not b
        fprintf(fid, ['\n  if ('])
        if not a
          fprintf(fid,[Servc.name{k},'(i) <= ',Servc.name{k},'_max(i)'])
        else
          fprintf(fid,'(')
        if not a  and  not b
          fprintf(fid,'  or  '); end
        if not b
          fprintf(fid,[Servc.name{k},'(i) >= ',Servc.name{k},'_min(i))'])
        else
          fprintf(fid,')')
        fprintf(fid,'\n  end')

# *********************************************************************
# differential & service equations
if not isempty(state_eq)
  if Comp.init  or  not isempty(algeb_eq)
    fprintf(fid, '\n\n case 3 %% differential equations\n')
  else
    fprintf(fid, '\n\nswitch flag\n case 3 %% differential equations\n')

for i in range(1, Servc.neq+1):
  Temp = Servc.type{i}
  if strcmp(Temp,'Inner')
    s_eq = vectorize(Servc.eq{i})
    fprintf(fid,['\n  ',Servc.name{i},' = ',s_eq,';'])
    if not strcmp(Servc.limit{i,1},'None')
      fprintf(fid, ['\n  ',Servc.name{i}, ...
                    ' = min(',Servc.name{i},',',Servc.name{i},'_max);'])
    if not strcmp(Servc.limit{i,2},'None')
      fprintf(fid, ['\n  ',Servc.name{i}, ...
                    ' = max(',Servc.name{i},',',Servc.name{i},'_min);'])

for i in range(1, State.n+1):
  if strcmp(State.nodyn{i},'Yes')
    fprintf(fid, ['\n  no_dyn_',State.name{i},' = find(',State.time{i},' == 0);'])
    fprintf(fid, ['\n  ', State.time{i}, '(no_dyn_',State.name{i},') = 1;'])
  if strcmp(State.time{i},'None')
    s_eq = vectorize(State.eq{i})
  else
    s_eq = vectorize(['(',State.eq{i},')/',State.time{i}])
  fprintf(fid, ['\n  DAE.f(',c_name,'.',State.name{i},') = ',s_eq,';'])

  if strcmp(State.nodyn{i},'Yes')
    fprintf(fid, ['\n  DAE.f(',c_name,'.',State.name{i},'(no_dyn_',State.name{i},')) = 0;'])

if State.n > 0; if strcmp(State.nodyn{State.n},'Yes'); fprintf(fid, '\n'); end; end

# set hard limits
fprintf(fid,'\n  %% non-windoup limits')
limfor1 = '\n  idx = find(%s >= %s_max  and  DAE.f(%s) > 0);'
limfor2 = '\n  if idx, DAE.f(%s(idx)) = 0; end'
limfor3 = '\n  DAE.x(%s) = min(%s,%s_max);'
limfor4 = '\n  idx = find(%s <= %s_min  and  DAE.f(%s) < 0);'
limfor5 = '\n  DAE.x(%s) = max(%s,%s_min);'
for i in range(1, State.n+1):
  varidx = [c_name,'.',State.name{i}]
  a = strcmp(State.limit{i,1},'None')
  if not a
    fprintf(fid,limfor1,State.name{i},State.name{i},varidx)
    fprintf(fid,limfor2,State.name{i})
    fprintf(fid,limfor3,varidx,State.name{i},State.name{i})
  b = strcmp(State.limit{i,2},'None')
  if not b
    fprintf(fid,limfor4,State.name{i},State.name{i},varidx)
    fprintf(fid,limfor2,State.name{i})
    fprintf(fid,limfor5,varidx,State.name{i},State.name{i})

fprintf(fid, '\n')

numdata = Initl.n
for i in range(1, Servc.neq+1):
  Temp = Servc.type{i}
  if okdata  and  strcmp(Temp,'Inner')
    numdata = numdata + 1
    fprintf(fid,['\n  ',c_name,'.dat(:,',int2str(numdata),') = ', Servc.name{i},';'])
  elseif strcmp(Temp,'Output')
    numdata = numdata + 1
    s_eq = vectorize(Servc.eq{i})
    TempT = [c_name,'.dat(:,',int2str(numdata),')']
    fprintf(fid,['\n  ',TempT,' = ',s_eq,';'])
    zz = ['z(',Servc.name{i},'_',Comp.name,'_idx)']
    if not strcmp(Servc.limit{i,1},'None')
      fprintf(fid, ['\n  ',TempT,' = min(',TempT,',',Servc.name{i},'_max);'])
    if not strcmp(Servc.limit{i,2},'None')
      fprintf(fid, ['\n  ',TempT,' = max(',TempT,',',Servc.name{i},'_min);'])
    fprintf(fid,['\n  ',zz,' = ',zz,' + ',TempT,';'])

fprintf(fid, '\n')

# *********************************************************************
# state variable Jacobians
if not isempty(state_eq)
  fprintf(fid, '\n\n case 4 %% state variable Jacobians\n')

# DAE.Fx
for j in range(1, State.n+1):
  if strcmp(State.nodyn{j},'Yes')
    fprintf(fid, ['\n  no_dyn_',State.name{j},' = find(',State.time{j},' == 0);'])
    fprintf(fid, ['\n  ', State.time{j}, '(no_dyn_',State.name{j},') = 1;'])
fprintf(fid, '\n')
if State.n, fprintf(fid,'\n  %% DAE.Fx'); end
fxformat = '\n  DAE.Fx = DAE.Fx + sparse(%s,%s,%s,DAE.n,DAE.n);'
for j in range(1, State.n+1):
  x_idx1 = [c_name,'.',State.name{j}]
for i in range(1, State.n+1):
    x_idx2 = [c_name,'.',State.name{i}]
    if strcmp(State.time{j},'None')   and  not strcmp(char(Fx(j,i)),'0')
      fxexp = vectorize(char(Fx(j,i)))
    else
      fxexp = ['(',vectorize(char(Fx(j,i))),')./',State.time{j}]
    if not strcmp(fxexp,['(0)./',State.time{j}])
      fprintf(fid,fxformat,x_idx1,x_idx2,fxexp)

fprintf(fid,'\n')

# DAE.Fy
if State.n  and  Algeb.n, fprintf(fid,'\n  %% DAE.Fy'); end
fyformat = '\n  DAE.Fy = DAE.Fy + sparse(%s,%s,%s,DAE.n,DAE.m);'
for j in range(1, State.n+1):
  x_idx1 = [c_name,'.',State.name{j}]
for i in range(1, Algeb.n+1):
    type = Algeb.name{i}
    if strcmp(type(1),'V')
      if Buses.n == 1
        x_idx2 = [c_name,'.bus','','+Bus.n']
      else
        x_idx2 = [c_name,'.bus',type(2:len(type)),'+Bus.n']
    elseif strcmp(type(1:5),'theta')
      if Buses.n == 1
        x_idx2 = [c_name,'.bus','']
      else
        x_idx2 = [c_name,'.bus',type(6:len(type))]
    if strcmp(State.time{j},'None')  and  not strcmp(char(Fy(j,i)),'0')
      fyexp = vectorize(char(Fy(j,i)))
    else
      fyexp = ['(',vectorize(char(Fy(j,i))),')./',State.time{j}]
    if not strcmp(fyexp,['(0)./',State.time{j}])
      fprintf(fid,fyformat,x_idx1,x_idx2,fyexp)

fprintf(fid,'\n')

# DAE.Gx
if State.n  and  Algeb.n, fprintf(fid,'\n  %% DAE.Gx'); end
gxformat = '\n  DAE.Gx = DAE.Gx + sparse(%s,%s,%s,DAE.m,DAE.n);'
for j in range(1, Algeb.neq+1):
  if not strcmp(Algeb.eq{1},'null')
    type = Algeb.eqidx{j,1}
    if strcmp(type(1),'P')
      if Buses.n == 1
        a_idx = [c_name,'.bus','']
      else
        a_idx = [c_name,'.bus',type(2:len(type))]
    elseif strcmp(type(1),'Q')
      if Buses.n == 1
        a_idx = [c_name,'.bus','','+Bus.n']
      else
        a_idx = [c_name,'.bus',type(2:len(type)),'+Bus.n']
for h in range(1, State.n+1):
      x_idx = [c_name,'.',State.name{h}]
      algexp = vectorize(char(Gx(j,h)))
      if not strcmp(algexp,'0')
        fprintf(fid,gxformat,a_idx,x_idx,algexp)

#if State.n > 0, fprintf(fid, ['\n\n  end']); end

# ***************************************************************
# non-windup limiters
if n_xmax  or  n_xmin
  fprintf(fid, '\n\n case 5 %% non-windup limiters\n')
for i in range(1, State.n+1):
    M = not strcmp(State.limit{i,1},'None')
    m = not strcmp(State.limit{i,2},'None')
    if M  or  m
      fprintf(fid, ['\n  idx = find(('])
      if M, fprintf(fid,'%s >= %s_max',State.name{i},State.name{i}); end
      if M  and  m; fprintf(fid,'  or  '); end
      if m, fprintf(fid,'%s <= %s_min',State.name{i},State.name{i}); end
      fprintf(fid,[')  and  DAE.f(',c_name,'.%s) == 0);'],State.name{i})
      fprintf(fid, '\n  if ~isempty(idx)')
      fprintf(fid,['\n    k = ',c_name,'.%s(idx);'],State.name{i})
      fprintf(fid,['\n    DAE.tn(k) = 0;'])
      fprintf(fid,['\n    DAE.Ac(:,k) = 0;'])
      fprintf(fid,['\n    DAE.Ac(k,:) = 0;'])
      fprintf(fid,['\n    DAE.Ac = DAE.Ac - sparse(k,k,1,DAE.m+DAE.n,DAE.m+DAE.n);'])
      fprintf(fid,['\n  end'])

fprintf(fid, '\n\nend\n')

# *******************************************************************
# warning message function
fprintf(fid,'\n\n%% -------------------------------------------------------------------')
fprintf(fid,'\n%% function for creating warning messages')
fprintf(fid,['\nfunction ',Comp.name,'warn(idx, msg)'])
#fprintf(fid,['\nglobal ',c_name]);
fprintf(fid,['\nfm_disp(fm_strjoin(''Warning: ',upper(Comp.name),' #'',int2str(idx),msg))'])

# close component file and return
fclose(fid)
fm_choice(['Function "fm_',Comp.name,'" built.'],2)

# ****************************************************************
function vect = varvect(vect,sep)

n = len(sep)-1
if iscell(vect)
  vect = fm_strjoin(vect,'#')
  vect = strrep([vect{:}],'#',sep)
  vect(end-n:end) = []