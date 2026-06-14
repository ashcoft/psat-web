# Module: psat.gui.fm_install
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_install():

# FM_INSTALL install an user defined component
#
# FM_INSTALL
#
#see also FM_UNINSTALL, FM_MAKE, FM_BUILD
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    22-Feb-2004
#Version:   1.0.1
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Algeb Buses Initl Param Servc State
global Comp Fig Path

# some settings
error_vect = []
error_number = 0
lasterr('')
string_update = cell(14,1)

if exist(['fm_',Comp.name,'.m']) == 2
  string_update{1,1} = ['Component File "fm_', Comp.name,'.m".']
else
  fm_choice(['Before updating system files, make sure that the ' ...
                 'component function is in the PSAT path.'],2)
  return

if not ishandle(Fig.update); fm_update; end
hdl_list = findobj(Fig.update,'Tag','Listbox1')

# structure and file names
c_name = lower(Comp.name)
c_name(1) = upper(c_name(1))
f_name = ['fm_',lower(Comp.name)]

okdata = 0
n_serv = 0
for i in range(1, Servc.n+1):
  if not strcmp(Servc.type{i},'Input')
    okdata = 1
    n_serv = n_serv + 1

# **********************************************************************
# update file comp.ini
fid = fopen([Path.psat,'comp.ini'], 'rt+')
if fid == -1
  fm_print('Cannot open file "comp.ini". Check permissions.')
update = 1
algeq = 0
limit = 0
for i in range(1, len(Algeb.eq)+1):
  if not strcmp(Algeb.eq{i,1},'null'),
    algeq = 1
    break
for i in range(1, State.n+1):
  if not strcmp(State.limit{i,1},'None')  or  not strcmp(State.limit{i,2},'None')
    limit = 1
    break

while 1
  sline = fgetl(fid)
  if not ischar(sline), break; end
  sline = [sline,blanks(len(f_name))]
  if strmatch(f_name,sline(1:len(f_name)),'exact')
    update = 0
    break
if update
  count = fseek(fid,0,'eof')
  b = [c_name,blanks(20)]
  b = b(1:20)
  if algeq,      c = '1 1 ';      else, c = '0 0 ';      end
  if State.n,    c = [c, '1 1 ']; else, c = [c, '0 0 ']; end
  if limit,      c = [c, '1 '];   else, c = [c, '0 '];   end
  if Comp.init,  c = [c, '0 1'];  else, c = [c, '1 0'];  end
  if Comp.shunt, c = [c, ' 1'];   else, c = [c, ' 0'];   end
  if Comp.series,c = [c, ' 1'];   else, c = [c, ' 0'];   end
  fprintf(fid,['\n%s %s'],b,c)
  comp_prop = num2str(['[',c,']'])
fclose(fid)

string_update{2,1} = 'Data File "comp.ini" updated.'
set(hdl_list,'String',string_update)

# **********************************************************************
# update function "fm_ncomp.m"
try
  if strcmp(Path.psat(1),'~')
    pathname = [getenv('HOME'),Path.psat(2:end)]
  else
    pathname = Path.psat
  file = textread([pathname,'fm_ncomp.m'], ...
                  '%s','delimiter','\n','whitespace','')
  idx1 = strmatch('check = 1;',file,'exact')
  idx2 = strmatch(['  ',c_name,'.n'],file)
  if isempty(idx2)
    file{idx1,1} = []
    file{end+3} = ['global ',c_name]
    file{end+1} = sprintf('if ~isempty(%s.con)',c_name)
    file{end+1} = sprintf('  %s.n = length(%s.con(:,1));',c_name, ...
                          c_name)
    if Buses.n == 1
      file{end+1} = sprintf('  %s.bus = Bus.int(round(%s.con(:,1)));', ...
                            c_name,c_name)
    else
for i in range(1, Buses.n+1):
        file{end+i} = sprintf('  %s.%s = Bus.int(round(%s.con(:,%d)));', ...
                              c_name,Buses.name{i},c_name,i)
    if Initl.n  or  okdata
      file{end+1} = sprintf('  %s.dat = zeros(%s.n,%d);', ...
              c_name,c_name,Initl.n+n_serv)
    file{end+1} = 'end'
    file{end+1} = ' '
    file{end+1} = 'check = 1;'
    fid = fopen([Path.psat,'fm_ncomp.m'], 'wt')
    for i=1:len(file)-1, fprintf(fid,'%s\n',file{i,1}); end
    fprintf(fid,'%s',file{end,1})
    fclose(fid)
catch
  fm_print('Cannot rewrite file "fm_ncomp.m". Check file permissions and content.')
  return
string_update{3,1} = 'System file "fm_ncomp.m" updated.'
set(hdl_list,'String',string_update)

# *********************************************************************
# update function "fm_inilf.m"
fid = fopen([Path.psat,'fm_inilf.m'], 'rt+')
if fid == -1
  fm_print('Cannot open file "fm_inilf.m". Check permissions.')
update = 1

while 1
  sline = fgetl(fid)
  if not ischar(sline)
    break
  if findstr([c_name,'.con'],sline)
    update = 0
    break
if update
  fseek(fid,0,'eof')
  fprintf(fid,'\n\n%s.con = [];',c_name)
  fprintf(fid,'\n%s.n = 0;',c_name)
  if Buses.n == 1
    fprintf(fid,'\n%s.bus = [];',c_name)
  else
for i in range(1, Buses.n+1):
      fprintf(fid,'\n%s.%s = [];',c_name,Buses.name{i})
  if Initl.n  or  okdata
    fprintf(fid,'\n%s.dat = [];',c_name)
for i in range(1, State.n+1):
    fprintf(fid,'\n%s.%s = [];',c_name,State.name{i,1})

fclose(fid)
string_update{4,1} = 'System file "fm_inilf.m" updated.'
set(hdl_list,'String',string_update)

# **********************************************************************
# update function "fm_var.m"
fid = fopen([Path.psat,'fm_var.m'], 'rt+')
if fid == -1
  fm_print('Cannot open file "fm_var.m". Check permissions.')
update = 1

while 1
  sline = fgetl(fid)
  if not ischar(sline)
    break
  if strmatch(['global ',c_name],sline,'exact')
    update = 0
    break
if update
  fseek(fid,0,'eof')
  fprintf(fid,['\n\n%%     ',Comp.descr,'\nglobal ',c_name])

fclose(fid)
string_update{5,1} = 'System file "fm_var.m" updated.'
set(hdl_list,'String',string_update)

# ***********************************************************************
# update file "namevarx.ini"
fid = fopen([Path.psat,'namevarx.ini'], 'rt+')
if fid == -1
  fm_print('Cannot open file "namevarx.ini". Check permissions.')

for i in range(1, State.n+1):
  update = 1
  fseek(fid,0,'bof')
  while 1
    sline = fgetl(fid)
    if not ischar(sline), break; end
    if not isempty(findstr(c_name,sline))  and  ...
          not isempty(findstr(State.fn{i,1},sline))
      update = 0
      break
  if update
    fseek(fid,0,'eof')
    nome1 = [State.un{i,1},blanks(19)]
    nome2 = [State.fn{i,1},blanks(19)]
    fprintf(fid,'\n%s %s %s',nome1(1:19),nome2(1:19),c_name)

fclose(fid)
string_update{6,1} = 'Data file "namevarx.ini" updated.'
set(hdl_list,'String',string_update)

# ************************************************************************
# update functions "fm_dynlf.m"  and  "fm_dynidx.m"
if State.n > 0
  if not Comp.init
    fid = fopen([Path.psat,'fm_dynlf.m'], 'rt+')
    if fid == -1
      fm_print('Cannot open file "fm_dynlf.m". Check permissions.')
    update = 1
    while update
      sline = fgetl(fid)
      if not ischar(sline), break; end
      if findstr([c_name,'.n'],sline); update = 0; end
    if update
      fseek(fid,0,'eof')
      fprintf(fid,'\n\nglobal %s',c_name)
      fprintf(fid,'\nif %s.n',c_name)
      fprintf(fid,'\n  for i = 1:%s.n',c_name)
for i in range(1, State.n+1):
        fprintf(fid,'\n    %s.%s(i) = DAE.n + %d;', ...
                c_name,State.name{i,1},i)
      fprintf(fid,'\n    DAE.n = DAE.n + %d;',State.n)
      fprintf(fid,'\n  end')
      fprintf(fid,'\nend')
    fclose(fid)
    string_update{7,1} = 'System file "fm_dynlf.m" updated.'
    string_update{8,1} = 'Updating of "fm_dynidx.m is not required.'
    set(hdl_list,'String',string_update)
  else
    fid = fopen(['fm_dynidx.m'], 'rt+')
    if fid == -1
      fm_print('Cannot open file "fm_dynidx.m". Check permissions.')
    update = 1
    while 1
      sline = fgetl(fid)
      if not ischar(sline), break; end
      if findstr([c_name,'.n'],sline); update = 0; break; end
    if update
      fseek(fid,0,'eof')
      fprintf(fid,'\n\nglobal %s',c_name)
      fprintf(fid,'\nif %s.n',c_name)
for i in range(1, State.n+1):
        fprintf(fid,'\n  %s.%s = zeros(%s.n,1);',c_name,State.name{i,1},c_name)
      fprintf(fid,'\n  for i = 1:%s.n',c_name)
for i in range(1, State.n+1):
        fprintf(fid,'\n    %s.%s(i) = DAE.n + %d;',c_name, State.name{i,1},i)
      fprintf(fid,'\n    DAE.n = DAE.n + %d;',State.n)
      fprintf(fid,'\n  end')
      fprintf(fid,'\nend')
    fclose(fid)
    string_update{8,1} = 'System file "fm_dynidx.m" updated.'
    string_update{7,1} = 'Updating of "fm_dynlf.m is not required.'
    set(hdl_list,'String',string_update)
else
  string_update{8,1} = 'Updating of "fm_dynidx.m" is not required (no state variables).'
  string_update{7,1} = 'Updating of "fm_dynlf.m is not required (no state variables).'
  set(hdl_list,'String',string_update)

# ***********************************************************************
# update file "Contents.m"
fid = fopen([Path.psat,'Contents.m'], 'rt+')
if fid == -1
  fm_print('Cannot open file "Contents.m". Check permissions.')
update = 1
while 1
  sline = fgetl(fid)
  if not ischar(sline), break; end
  sline = [sline,blanks(len(f_name)+4)]
  sline = sline(1:len(f_name)+4)
  if not isempty(findstr(sline,['%   ',f_name]))
    update = 0
    break
if update
  fseek(fid,0,'eof')
  fprintf(fid,'\n%%   %s  - %s',f_name,Comp.descr)
fclose(fid)
string_update{9,1} = 'Contents file for on line help updated.'
set(hdl_list,'String',string_update)

# **********************************************************************
# update file "service.ini"
fid = fopen([Path.psat,'service.ini'], 'rt+')
if fid == -1
  fm_print('Cannot open file "service.ini". Check permissions.')
for i in range(1, Servc.n+1):
  update = 1
  fseek(fid,0,'bof')
  if strcmp(Servc.type{i,1},'Input')
    while 1
      sline = fgetl(fid)
      sline = [sline,blanks(len(Servc.name{i}))]
      if not ischar(sline)
        break
      if findstr(Servc.name{i},sline(1:len(Servc.name{i})))
        update = 0
        break
    if update
      fseek(fid,0,'eof')
      fprintf(fid,['\n',Servc.name{i,1}])
fclose(fid)
string_update{10,1} = 'File Data "service.ini" updated.'
set(hdl_list,'String',string_update)

# ***********************************************************************
# update function "fm_xfirst.m"
if State.n  and  not Comp.init
  fid = fopen([Path.psat,'fm_xfirst.m'], 'rt+')
  if fid == -1
    fm_print('Cannot open file "fm_xfirst.m". Check permissions.')
  update = 1

  while 1
    sline = fgetl(fid)
    if not ischar(sline), break; end
    if not isempty(findstr([c_name,'.n'],sline))
      update = 0
      break
  if update
    fseek(fid,0,'eof')
    fprintf(fid,'\n\nglobal %s',c_name)
    fprintf(fid,'\nif %s.n',c_name)
for i in range(1, State.n+1):
      fprintf(fid,'\n  DAE.x(%s.%s) = %s*ones(%s.n,1);', ...
              c_name,State.name{i,1},State.init{i,1},c_name)
    fprintf(fid,['\nend'])
  fclose(fid)
  string_update{11,1} = 'System file "fm_xfirst.m" updated.'
  set(hdl_list,'String',string_update)
else
  string_update{11,1} = 'Updating System file "fm_xfirst.m" not required.'
  set(hdl_list,'String',string_update)

# % ***********************************************************************
# if update
#   fseek(fid,0,'eof');
#   string = [c_name,blanks(15)];
#   fprintf(fid,['\n',string(1:15)]);
#   x_max = [1:State.n];
#   if State.n
#     x_idx = strmatch('None',State.limit(:,1),'exact');
#     x_max(x_idx) = [];
#   end
#   x_min = [1:State.n];
#   if State.n
#     x_idx = strmatch('None',State.limit(:,2),'exact');
#     x_min(x_idx) = [];
#   end
#   n_xmax = length(x_max); n_xmin = length(x_min);
#   s_max = [1:Servc.neq];
#   if Servc.n
#     s_idx = strmatch('None',Servc.limit(:,1),'exact');
#     s_max(s_idx) = [];
#   end
#   s_min = [1:Servc.neq];
#   if Servc.n
#     s_idx = strmatch('None',Servc.limit(:,2),'exact');
#     s_min(s_idx) = [];
#   end
#   n_smax = length(s_max); n_smin = length(s_min);
#   n_tot_param = 2 + Buses.n + Param.n + n_xmax + n_xmin + n_smax + n_smin;
#   fprintf(fid,['[repmat(''%%4d '',1,%d), ', ...
#                'repmat(''%%8.4f '',1,%d)]'],Buses.n,n_tot_param);
# end

# ***********************************************************************
# update function "psat.m"
fid = fopen([Path.psat,'psat.m'], 'rt+')
if fid == -1
  fm_print('Cannot open file "psat.m". Check permissions.')
update = 1
while 1
  sline = fgetl(fid)
  if not ischar(sline), break, end
  sline = [sline,blanks(len(f_name))]
  if not isempty(strmatch(c_name,sline(1:len(c_name)),'exact'))
    update = 0
    break
if update
  fseek(fid,0,'eof')
  fprintf(fid,'\n%% %s - %s',c_name,Comp.descr)
  fprintf(fid,'\n%s = struct(''con'',[],''n'',0,',c_name)
  okdata = 0
  for i = 1:Servc.n
    if not strcmp(Servc.type{i},'Input'); okdata = 1
      break
  if Initl.n  or  okdata
    fprintf(fid,'''dat'',[],',c_name)
  if Buses.n == 1
    fprintf(fid,'''bus'',[],')
  else
for i in range(1, Buses.n+1):
      fprintf(fid,'''%s'',[],',Buses.name{i})
for i in range(1, State.n-1+1):
    fprintf(fid,'''%s'',[],',State.name{i,1})
  fprintf(fid,'''%s'',[]);\n',State.name{State.n,1})
fclose(fid)
string_update{12,1} = 'System file "psat.m" updated.'
set(hdl_list,'String',string_update)

# ***********************************************************************************
# update function "closepsat.m"
fid = fopen([Path.psat,'closepsat.m'], 'rt+')
if fid == -1
  fm_print('Cannot open file "closepsat.m". Check permissions.')
update = 1

while 1
  sline = fgetl(fid)
  if not ischar(sline)
    break
  if strmatch(['clear ',c_name],sline,'exact')
    update = 0
    break
if update
  fseek(fid,0,'eof')
  fprintf(fid,['\n\n%%     ',Comp.descr,'\nclear ',c_name])

fclose(fid)
string_update{13,1} = 'System file "closepsat.m" updated.'
set(hdl_list,'String',string_update)


# **********************************************************************
# update structure Varname
Varname.unamex = ''
Varname.fnamex = ''
Varname.compx = ''
Varname.unamey = ''
Varname.fnamey = ''
Varname.compy = ''

failed = 0
fid = fopen([Path.psat,'namevarx.ini'], 'rt')
if fid == -1,
  failed = 1
else
  nname = 0
  while 1
    sline = fgetl(fid)
    if not ischar(sline), break; end
    try
      Varname.unamex{nname+1,1} = deblank(sline(1:20))
      Varname.fnamex{nname+1,1} = deblank(sline(21:40))
      Varname.compx{nname+1,1}  = deblank(sline(41:end))
      nname = nname + 1
  count = fclose(fid)
  string_update{14,1} = 'Structure "Varname" updated.'
if failed
  string_update{14,1} = 'Error: Structure "Varname" could not be updated.'
else
  string_update{14,1} = 'Structure "Varname" updated.'
set(hdl_list,'String',string_update)


# ***********************************************************************************
# update structure Comp
Comp.names = ''
Comp.prop = ''
Comp.n = 0
Comp.shunt = 1
Comp.series = 0
fid = fopen([Path.psat,'comp.ini'], 'rt')
if fid == -1,
  string_update{15,1} = 'Error: Structure "Comp" could not be updated.'
else
  ncomp=0
  while 1
    sline = fgetl(fid)
    if not ischar(sline), break; end
    try
      Comp.names{ncomp+1,1} = deblank(sline(1:21))
      Comp.prop(ncomp+1,:) = str2num(sline(22:38))
      ncomp=ncomp + 1
  count = fclose(fid)
  Comp.names{ncomp+1} = 'PV'
  Comp.prop(ncomp+1,:) = [2 1 0 0 0 1 0]
  Comp.names{ncomp+2} = 'SW'
  Comp.prop(ncomp+2,:) = [2 1 0 0 0 1 0]
  Comp.n = ncomp + 2
  string_update{15,1} = 'Structure "Comp" updated.'
set(hdl_list,'String',string_update)

# last operations
string_update{end+1,1} = 'Updating operations completed.'
set(hdl_list,'String',string_update)