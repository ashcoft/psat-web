# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_set.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_set(varargin):

# FM_SET define general settings and operations for
#        the main window and other utilities
#
#FM_SET(COMMAND)
#       COMMAND = 'lf' solves power flow
#       COMMAND = 'setdata' sets data file
#       COMMAND = 'opensys' load system
#       COMMAND = 'savesys' save current system
#       etc.
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    10-Feb-2003
#Update:    27-Feb-2003
#Version:   1.0.2
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings
fm_var

command = varargin{1}

switch command
 case 'colormap'

  map = [0         0         0
         0         0    0.5020
         0         0    1.0000
         0.5020         0         0
         0.5020         0    0.5020
         1.0000         0         0
         1.0000         0    1.0000
         0    0.5020         0
         0    0.7530    0.5020
         0.5020    0.5020         0
         0.5020    0.5020    0.5020
         0.7530    0.7530    0.7530
         0    1.0000         0
         0    0.7530    1.0000
         1.0000    1.0000         0
         1.0000    1.0000    1.0000]
  set(gcf,'ColorMap',map)

 case 'delete'

  Fig.main = -1
  Hdl.status = -1
  Hdl.text = -1
  Hdl.status = -1
  Hdl.frame = -1
  Hdl.bar = -1
  Hdl.axes = -1

 case 'keypress'

  hdl = findobj(gcbf,'Tag','EditCommand')
  tasto = get(Fig.main,'CurrentCharacter')
  if isempty(tasto), return, end
  switch double(tasto)
   case 13
    fm_set('command')
   case 8
    testo = get(hdl,'String')
    if len(testo) <= 1
      testo = ''
    else
      testo = testo(1:end-1)
    set(hdl,'String',testo)
   case 9
    set(hdl,'SelectionHighlight','on')
   case 127
    set(hdl,'String','')
   case 28
    stringa = get(hdl,'String')
    set(hdl,'String',stringa(1:end-1),'UserData',stringa)
   case 29
    stringa = get(hdl,'String')
    set(hdl,'String',stringa(1:end-1),'UserData',stringa)
   case 27
    fm_set('exit')
   case 30
    hdll = findobj(gcbf,'Tag','ListCommand')
    stringa = get(hdll,'String')
    value = max(get(hdll,'Value')-1,1)
        if not strcmp(stringa{value},'<empty>'),
          set(hdl,'String',stringa{value}),
          set(hdll,'Value',max(value,1))
   case 31
    hdll = findobj(gcbf,'Tag','ListCommand')
    stringa = get(hdll,'String')
    value = min(get(hdll,'Value')+1,len(stringa))
    if not strcmp(stringa{value},'<empty>'),
      set(hdl,'String',stringa{value}),
      set(hdll,'Value',max(value,1))
   otherwise
    set(hdl,'String',[get(hdl,'String'),tasto])

 case 'exit'

  uiwait(fm_choice('Quit PSAT?'))
  if Settings.ok,
    a = fieldnames(Fig)
for i in range(len(a), 1+1, -1):
      fig = getfield(Fig,a{i})
      if fig, close(fig), end

 case 'setdefault'

  uiwait(fm_choice('Set Default Values?'))
  if Settings.ok == 1
    hdl1 = findobj(gcbf,'Tag','EditText1')
    set(hdl1,'String','50')
    Settings.freq = 50
    hdl2 = findobj(gcbf,'Tag','EditText2')
    set(hdl2,'String','100')
    Settings.mva = 100
    hdl3 = findobj(gcbf,'Tag','EditText3')
    set(hdl3,'String','0')
    Settings.t0 = 0
    hdl4 = findobj(gcbf,'Tag','EditText4')
    set(hdl4,'String','30')
    Settings.tf = 30
    hdl5 = findobj(gcbf,'Tag','EditText5')
    set(hdl5,'String','1e-5')
    Settings.lftol = 1e-5
    hdl6 = findobj(gcbf,'Tag','EditText6')
    set(hdl6,'String','20')
    Settings.lfmit = 20
    hdl7 = findobj(gcbf,'Tag','EditText7')
    Settings.dyntol = 1e-5
    set(hdl7,'String','1e-5')
    hdl8 = findobj(gcbf,'Tag','EditText8')
    Settings.dynmit = 20
    set(hdl8,'String','20')

    Settings.vs = 0
    Settings.plot = 1
    Settings.red = 1
    Settings.showlf = 0
    Settings.dlf = 0
    Settings.dac = 0
    Settings.method = 2
    Settings.plottype = 1

    fm_print('Default parameter values set.')
  else
    fm_print('No parameter values resetting.')

 case 'savesys'

  if not Bus.n  or  not Settings.init
    fm_print('No system is loaded. ',2),
    return,
  fileout = fm_filenum('out')
  filedata = strrep(File.data,'@ ','')
  filepert = strrep(File.pert,'@ ','')

  pathdata = Path.data
  if strcmp(pathdata(1),'~')
    pathdata = [getenv('HOME'),pathdata(2:end)]

  pathpert = Path.pert
  if not isempty(Path.pert)
    if strcmp(pathpert(1),'~')
      pathpert = [getenv('HOME'),pathpert(2:end)]

  filedata = strrep(filedata,'(mdl)','_mdl')
  if Settings.matlab  and  Settings.hostver >= 7.14,
    Source.data = ...
        strvcat(textread([pathdata,deblank(filedata),'.m'], ...
                         '%s','delimiter', ...
                         '\n','whitespace',''))

    if not isempty(Path.pert)
      Source.pert = ...
          strvcat(textread([pathpert,deblank(filepert),'.m'], ...
                           '%s','delimiter', ...
                           '\n','whitespace',''))
  else
    Source.data = ...
        char(textread([pathdata,deblank(filedata),'.m'], ...
                      '%s','delimiter', ...
                      '\n','whitespace',''))

    if not isempty(Path.pert)
      Source.pert = ...
          char(textread([pathpert,deblank(filepert),'.m'], ...
                        '%s','delimiter', ...
                        '\n','whitespace',''))
  hdlpert = Hdl.pert
  Hdl.pert = ''
  save([pathdata,fileout,'.out'])
  Hdl.pert = hdlpert
  fm_disp
  fm_print(['System saved in "',Path.data,fileout,'.out"'])

 case 'closepert'

  fm_print(['Perturbation file "',Path.pert,File.pert,'" closed.'],1)
  Path.pert = ''
  File.pert = ''
  Source.pert = ''
  cd(Path.psat)
  if Settings.hostver >= 6
      Hdl.pert = str2func('pert')
  else
      Hdl.pert = 'pert'
  cd(Path.local)
  hdltext = findobj(Fig.main,'Tag','EditText10')
  set(hdltext,'String','','TooltipString','')

 case 'closedata'

  fm_print(['Data file "',Path.data,File.data,'" closed.'],1)
  Path.data = ''
  File.data = ''
  Source.data = ''
  hdltext = findobj(Fig.main,'Tag','EditText9')
  set(hdltext,'String','','TooltipString','')

 case 'savesettings'

  [fid,msg] = fopen([Path.psat,'settings.m'],'wt')
  if fid == -1
    fm_print(msg)
    return
  fields = fieldnames(Settings)
for i in range(1, len(fields)+1):
    if strcmp(fields{i},'color')
      continue
    value = eval(['Settings.',fields{i}])
    if isnumeric(value)
      cout = fprintf(fid,'Settings.%s = %s;\n',fields{i},num2str(value))
    else
      cout = fprintf(fid,'Settings.%s = ''%s'';\n',fields{i},value)
  fields = fieldnames(Theme)
for i in range(1, len(fields)+1):
    if strcmp(fields{i},'hdl')
      continue
    value = eval(['Theme.',fields{i}])
    if isnumeric(value)
      cout = fprintf(fid,'Theme.%s = [%s];\n',fields{i},num2str(value))
    else
      cout = fprintf(fid,'Theme.%s = ''%s'';\n',fields{i},value)
  cout = fprintf(fid,'Theme.hdl = zeros(18,1);\n')
  fclose(fid)

 case 'savedata'

  filedata = [File.data,'  ']
  if strcmp(filedata([1:2]),'@ ')
    filedata = deblank(strrep(filedata,'@ ',''))
    if isempty(Source.data),
      fm_print('Cannot restore the data file.'),
      return,
    a = dir([Path.data,'*.m'])
    b = {a.name}
    older = strmatch([filedata,'.m'],b,'exact')
    if not isempty(older)
      uiwait(fm_choice(['Overwrite Existing File "',filedata,'.m" ?']))
      if not Settings.ok,
        return,
    try
      fid = fopen([Path.data,filedata,'.m'],'wt')
      if fid == -1,
        fm_print(['Cannot write the data file. Check folder ' ...
                 'authorizations.'],2),
        return,
    catch
      fm_print(['Cannot write the data file.  Check folder ' ...
               'authorizations.'],2)
      return
    rowc = len(Source.data(1,:))
    count = fprintf(fid,[repmat('%c',1,rowc),' \n'],Source.data');
    fclose(fid)
    fm_print(['Data file stored in "',Path.data,filedata,'.m"'])
    File.data = filedata
    hdltext = findobj(Fig.main,'Tag','EditText9')
    set(hdltext, ...
        'String',File.data, ...
        'TooltipString',[Path.data,File.data])

  else
    fm_print('The current data file is already saved.')

 case 'close'

  stringa = get(findobj(Fig.main,'Tag','PushClose'),'String')
  if strcmpi(stringa(end-3:end),'stop')
    set(Fig.main,'UserData',0)
  else
    close(Fig.main)

 case 'opensys'

  if clpsat.init  and  nargin > 1
    file = varargin{2}
    pathname = varargin{3}
  else
    if not isempty(Path.data), cd(Path.data); end
    [file,pathname] = uigetfile('d*.out',['Select System Data ' ...
                        'File'])

  fm_disp
  if pathname != 0

    path2 = Path
    fig2 = Fig
    hdl2 = Hdl
    file2 = File
    history2 = History
    theme2 = Theme
    load([pathname,file],'-mat')

    dfile = strrep(file,'.out','.m')
    pfile = ''
    if not isempty(Source.pert)
      pfile = strrep(file,'.out','.m')
      pfile(1) = 'p'

    fid = fopen([pathname,dfile],'wt+')
    if fid == -1,
      fm_print(['Cannot write the data file. Check folder ' ...
               'authorizations.'],2),
    else
      rowc = len(Source.data(1,:))
      count = fprintf(fid,[repmat('%c',1,rowc),' \n'],Source.data');
      fclose(fid)
    if not isempty(pfile)
      fid = fopen([pathname,pfile],'wt+')
      if fid == -1,
        fm_print(['Cannot write the disturbance file. Check folder ' ...
                 'authorizations.'],2),
      else
        rowc = len(Source.pert(1,:))
        count = fprintf(fid,[repmat('%c',1,rowc),' \n'],Source.pert');
        fclose(fid)
        cd(pathname)
        if Settings.hostver >= 6
            Hdl.pert = str2func(pfile(1:end-2))
        else
            Hdl.pert = pfile(1:end-2)
        cd(Path.local)

    hdl_data = findobj(fig2.main,'Tag','EditText9')
    hdl_pert = findobj(fig2.main,'Tag','EditText10')
    Fig = fig2
    hdlpert = Hdl.pert
    Hdl = hdl2
    Hdl.pert = hdlpert
    History = history2
    Theme = theme2
    if not isempty(File.pert),
      File.pert = ['@ ',pfile(1:end-2)]
#File.pert = strrep(File.pert,'@ @ ','@ ');
    File.data = ['@ ',dfile(1:end-2)]
#File.data = strrep(File.data,'@ @ ','@ ');

    set(hdl_data, ...
        'String',File.data, ...
        'ForegroundColor',[0 0 0.592], ...
        'TooltipString',[Path.data,File.data])
    set(hdl_pert, ...
        'String',File.pert, ...
        'ForegroundColor',[0 0 0.592], ...
        'TooltipString',[Path.pert,File.pert])

    Path.psat = path2.psat
    Path.build = path2.build
    Path.local = path2.local
    Path.images = path2.images
    Path.themes = path2.themes
    Path.data = pathname
    if not isempty(File.pert)
      Path.pert = pathname
    else
      Path.pert = ''

    if ishandle(Fig.plot) > 0,
      close(Fig.plot),
      Fig.plot = -1
    fm_print(['System ',pathname, file,' loaded.'])

  else
    fm_print('No loaded system or not existent directory',2)

 case 'opensim'

  [filename, pathname] = uigetfile( ...
      '*.mdl', ...
      'Pick a Simulink Model')
  if not pathname, return, end
  cd(pathname)
  if exist(filename) != 4
    fm_print('The selected file is not a Simulink model.',2)
    cd(Path.local)
    return
  open_system(filename(1:end-4))
  cd(Path.local)

 case 'setdata'

  Path.temp = Path.data
  File.temp = File.data

  if ishandle(Fig.dir)
    set(Fig.dir,'Name','Load Data File')
    hdl = findobj(Fig.dir,'Tag','Pushbutton1')
    set(hdl,'String','Load','Callback','fm_dirset openfile')
    hdl = findobj(Fig.dir,'Tag','Listbox2')
    set(hdl,'Max',0,'ButtonDownFcn','fm_dirset openfile','Value',1)
    hdl = findobj(Fig.dir,'Tag','Pushbutton3')
    set(hdl,'Callback','fm_dirset cancel','String','Cancel')
  else
    fm_dir(1)
  uiwait(Fig.dir)

  if Path.temp == 0
    fm_print(['No data file has been selected or file does not exist'],2)
    return

  if strcmp(computer,'GLNX86'),
    Path.temp = strrep(Path.temp,getenv('HOME'),'~')

  if exist([Path.temp,File.temp(1:end-2)]) == 4 ...
         and  strcmp(File.temp(end-1:end),'.m')
    fm_choice(['Simulink model with the same name of the ', ...
               'selected data exists. No file set.'],2)
    fm_print('No file data set.',2)
  else
    File.data = File.temp
    Path.data = Path.temp
    a = dir([Path.data,File.data])
    if isempty(a)
      fm_print(['File "',File.data,'" does not exist.'],2)
      return
    else
      File.modify = a.date
    if not isempty(findstr(File.data,'.mdl'))
# make sure that the file name does not start with a number
      first = double(File.data(1))
      if first <= 57  and  first >= 48
        localpath = pwd
        cd(Path.data)
        if exist(['d',File.data]) != 4
          copyfile(File.data,['d',File.data])
        cd(localpath)
        File.data = ['d',File.data]
      exist(File.data(1:end-4))
      File.data = strrep(File.data,'.mdl','(mdl)')
    File.data = strrep(File.data,'.m','')
    hdltext = findobj(Fig.main,'Tag','EditText9')
    set(hdltext,'String',File.data, ...
                'TooltipString',[Path.data,File.data])
    if not isempty(findstr(File.data,'(mdl)'))
      set(hdltext,'ForegroundColor',[0 0.592 0])
    else
      set(hdltext,'ForegroundColor',Theme.color07)
    fm_print(['Data file "',Path.data,File.data,'" set'],1)
    Settings.init = 0
  if ishandle(Fig.plotsel), close(Fig.plotsel), end

 case 'setpert'

  Path.temp = Path.pert
  File.temp = File.pert

  if ishandle(Fig.dir)
    set(Fig.dir,'Name','Load Data File')
    hdl = findobj(Fig.dir,'Tag','Pushbutton1')
    set(hdl,'String','Load','Callback','fm_dirset openfile')
    hdl = findobj(Fig.dir,'Tag','Listbox2')
    set(hdl,'Max',0,'ButtonDownFcn','fm_dirset openfile','Value',1)
    hdl = findobj(Fig.dir,'Tag','PopupMenu1')
    set(hdl,'Enbale','inactive','Value',3)
    hdl = findobj(Fig.dir,'Tag','Pushbutton3')
    set(hdl,'Callback','fm_dirset cancel','String','Cancel')
  else
    fm_dir(2)

  uiwait(Fig.dir)

  if Path.temp == 0
    fm_print('No perturbation file selected or file does not exist',2)
  else
    Path.pert = Path.temp
    File.pert = File.temp
    if strcmp(computer,'GLNX86'),
      Path.pert = strrep(Path.pert,getenv('HOME'),'~')
    cd(Path.pert)
    lfile = len(File.pert)
    File.pert = File.pert(1:lfile-2)
    if Settings.hostver >= 6
      Hdl.pert = str2func(File.pert)
    else
      Hdl.pert = File.pert
    cd(Path.local)
    hdltext = findobj(Fig.main,'Tag','EditText10')
    set(hdltext,'String',File.pert, ...
                'ForegroundColor',Theme.color07, ...
                'TooltipString',[Path.pert,File.pert])
    fm_print(['Perturbation file "',Path.pert,File.pert,'" set'],1)

 case 'command'

  hdl = findobj(gcbf,'Tag','EditCommand')
  stringa = get(hdl,'String')
  set(hdl,'String','')
  hdl = findobj(gcbf,'Tag','ListCommand')
  comandi = get(hdl,'String')
  if strcmp(comandi{1},'<empty>'),
    comandi{1,1} = stringa
  else,
    comandi{end+1,1} = stringa
  if len(comandi) > 100, comandi(1) = []; end
  set(hdl,'String',comandi,'Value',len(comandi))
  if strcmp(stringa,'command'),
    fm_print('Invalid command',2),
    return,
  if strcmp(stringa,'<empty>'), return, end
  try
    try,
      eval(['fm_set ',stringa])
    catch,
      eval(stringa)
      fm_print(['Command "',stringa,'" executed.'])
  catch
    fm_print(lasterr,2)

 case 'listcommand'

  if strcmp(get(Fig.main,'SelectionType'),'open')
    hdl = findobj(gcbf,'Tag','ListCommand')
    stringa = get(hdl,'String')
    value = get(hdl,'Value')
    hdl = findobj(gcbf,'Tag','EditCommand')
    set(hdl,'String',stringa{value})
    fm_set('command')

 case 'lf'

  if isempty(File.data),
    fm_print('Set a data file before running Power Flow.',2),
    return,

  if Settings.freq <= 0
    Settings.freq = 50
    if ishandle(Fig.main)
      hdl = findobj(Fig.main,'Tag','EditText1')
      set(hdl,'String',num2str(Settings.freq))
  if Settings.mva <= 0
    Settings.mva = 100
    if ishandle(Fig.main)
      hdl = findobj(Fig.main,'Tag','EditText2')
      set(hdl,'String',num2str(Settings.mva))

  filedata = strrep([File.data,'  '],'@ ','')

  if not isempty(findstr(filedata,'(mdl)'))
    filedata1 = File.data(1:end-5)
    open_sys = find_system('type','block_diagram')
    OpenModel = sum(strcmp(open_sys,filedata1))
    if OpenModel
      if strcmp(get_param(filedata1,'Dirty'),'on')  or  ...
            str2num(get_param(filedata1,'ModelVersion')) > Settings.mv,
        check = sim2psat
        if not check, return, end
  try
    cd(Path.data)
  catch
    fm_print('Data folder does not exist (maybe it was removed).',2)
    return
  filedata = deblank(strrep(filedata,'(mdl)','_mdl'))
  a = exist(filedata)
  if not a
    fm_print('Data file does not exist (maybe it was removed).',2)
    cd(Path.local)
    return

  if a == 2,
    lasterr('')
    b = dir([filedata,'.m'])
#if ~strcmp(File.modify,b.date)  or  clpsat.readfile
    if clpsat.readfile
      try
        fm_inilf
        clear(filedata)
        eval(filedata)
        File.modify = b.date
      catch
        fm_print(lasterr),
        fm_print(['Something wrong with the data file "',filedata,'"']),
        cd(Path.local)
        return
  else
    fm_print(['File "',filedata,'" not found or not an m-file'],2)
  cd(Path.local)

  if Settings.static #  do not use dynamic components
for i in range(1, Comp.n+1):
      comp_con = [Comp.names{i},'.con']
      comp_ext = eval(['~isempty(',comp_con,')'])
      if comp_ext  and  not Comp.prop(i,6)
        eval([comp_con,' = [];'])

# the following code is needed for compatibility with older PSAT versions

  if isfield(Varname,'bus')
    if not isempty(Varname.bus)
      Bus.names = Varname.bus
      Varname = rmfield(Varname,'bus')

  if exist('Mot')
    if isfield(Mot,'con')
      Ind.con = Mot.con
      clear Mot

# end of compatibility code %

  if ishandle(Fig.main)
    hdl = findobj(Fig.main,'Tag','EditText3')
    time0 = str2num(get(hdl,'String'))
    if time0 != Settings.t0,
      set(hdl,'String',num2str(Settings.t0)),
      fm_print(['Initial simulation time "t0" set to ',num2str(Settings.t0),' s'])
    hdl = findobj(Fig.main,'Tag','EditText4')
    timef = str2num(get(hdl,'String'))
    if timef != Settings.tf,
      set(hdl,'String',num2str(Settings.tf)),
      fm_print(['Final simulation time "tf" set to ',num2str(Settings.tf),' s'])
    set(Fig.main,'Pointer','watch')

  Settings.init = 0
  fm_spf
  if ishandle(Fig.main), set(Fig.main,'Pointer','arrow'); end
  SNB.init = 0
  LIB.init = 0
  CPF.init = 0
  OPF.init = 0

# ---------------------------------------------------------------------------
#case 'stabrep'
#for i = 1:Bus.n;  [Istab(i),Vnew(i),angnew(i)]= fm_stab(i,0);
#end
#fid = fopen([Path.data,'vstab.txt'], 'wt');
#count = fprintf(fid, 'Voltage Stability Index at Network
#Buses\n\n');
#count = fprintf(fid, '#bus         Index       V    phase\n\n');
#for i = 1:Bus.n
#    count = fprintf(fid,[fvar(Bus.names{i},12),
#    fvar(Istab(i),12), ...
#                         fvar(Vnew(i),12),
#                         fvar(angnew(i),12),'\n']);
#end
#count = fclose(fid);
#fm_text(13,[Path.data,'vstab.txt'])
# ---------------------------------------------------------------------------

 case 'opf'

  if max(OPF.lmin) > OPF.lmax
    fm_print('Lambda_min must be less than Lambda_max.',2)
    return
  [ao,bo] = size(OPF.omega)
  [al,bl] = size(OPF.lmin)
  ao = ao*bo
  a1 = al*bl

  switch OPF.type
   case 1
    OPF.show = 1
    if ao > 1,
      fm_print(['Single OPF selected. Only the 1th value of ' ...
               'the weighting factor will be used.'])
    if a1 > 1,
      fm_print(['Single OPF selected. Only the 1th value ' ...
               'of the min load parameter will be used.'])
    OPF.w = OPF.omega(1)
    OPF.lmin = OPF.lmin(1)
    if ishandle(Fig.opf)
      hdl_omeg = findobj(Fig.opf,'Tag','EditText1')
      hdl_lmin = findobj(Fig.opf,'Tag','EditText2')
      set(hdl_omeg,'String',num2str(OPF.omega_s))
      set(hdl_lmin,'String',num2str(OPF.lmin))
    if OPF.w == 0,
      fm_opfm
    else,
      fm_opfsdr
   case 2
    if ao == 1,
      OPF.show = 1
      OPF.w = OPF.omega
      fm_print(['The weighting factor is scalar. Single OPF will be ' ...
               'run.'])
      if OPF.w == 0,
        fm_opfm
      else,
        fm_opfsdr
    else
      OPF.fun = 'fm_opfsdr'
      fm_pareto
   case 3,
    uiwait(fm_choice('Sorry! Daily forecast not implemented yet ...',2))
   case 4,
    fm_atc
   case 5,
    fm_atc

 case 'appendV'

  type = varargin{2}

  if isempty(File.data),
    fm_print('No data file loaded.',2),
    return,
  filedata = strrep(File.data,'@ ','')
  if Settings.init == 0,
    fm_print('Run power flow before saving voltages.',2),
    return,

  if isempty(strfind(filedata,'(mdl)'))
    fid = fopen([Path.data,filedata,'.m'],'r+')
    count = fseek(fid,0,1)
    switch type
     case 'flat'
      count = fprintf(fid, '\n\nBus.con(:,3) = 1;\n ')
      count = fprintf(fid, 'Bus.con(:,4) = 0;\n ')
      count = fprintf(fid, 'SW.con(:,10) = 0;\n ')
     otherwise
      count = fprintf(fid, '\n\n\nBus.con(:,3) = [...\n      ')
for i in range(1, Bus.n-1+1):
        count = fprintf(fid,'%10.7f;',DAE.y(Bus.v(i)))
        if rem(i,5) == 0
          count = fprintf(fid,'\n      ')
      count = fprintf(fid,'%10.7f];\n\n',DAE.y(Bus.v(Bus.n)))
      count = fprintf(fid, 'Bus.con(:,4) = [...\n      ')
for i in range(1, Bus.n-1+1):
        count = fprintf(fid, '%10.7f;',DAE.y(Bus.a(i)))
        if rem(i,5) == 0
          count = fprintf(fid,'\n      ')
      count = fprintf(fid,'%10.7f];\n\n',DAE.y(Bus.a(Bus.n)))
for i in range(1, SW.n+1):
        Pg = Settings.mva*Bus.Pg(SW.bus(i))/SW.con(i,2)
        count = fprintf(fid,'SW.con(%d,10) = %10.7f;\n',i,Pg)
    fclose(fid)
    fm_print(['Voltages appended in file "',Path.data,File.data,'"'])
  else
# load Simulink Library and update Bus blocks
    load_system('fm_lib')
    cd(Path.data)
    filedata = filedata(1:end-5)
    open_sys = find_system('type','block_diagram')
    if not sum(strcmp(open_sys,filedata))
      open_system(filedata)
    cur_sys = get_param(filedata,'Handle')
    blocks = find_system(gcs,'MaskType','Bus')
    if len(blocks) != Bus.n
      fm_print('The number of "Bus" blocks does not match current bus number',2)
      return
    switch type
     case 'flat'
for i in range(1, len(blocks)+1):
        set_param(blocks{i},'p3_4q','[1  0]')
     otherwise
for i in range(1, len(blocks)+1):
        set_param( ...
            blocks{i}, 'p3_4q', ...
            ['[',num2str([DAE.y(Bus.v(i)),DAE.y(Bus.a(i))]),']'])
    cd(Path.local)

 otherwise

  error('The string is not a valid command')

