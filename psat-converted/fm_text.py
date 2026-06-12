# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_text.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_text(varargin):

# FM_TEXT settings for the command history GUI
#
# FM_TEXT(VARARGIN)
#
# see also FM_HIST
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    11-Feb-2003
#Version:   1.0.2
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global History Fig Hdl Path Settings clpsat

if nargin == 1
  type = varargin{1}
elseif nargin == 2
  type = varargin{1}
  prop = varargin{2}
elseif nargin == 3
  type = varargin{1}
  prop = varargin{2}
  valu = varargin{3}
else
  fm_print('Improper number of arguments in calling function fm_text',2)
  return

switch type
 case 1

  filename  = [fm_filenum('log'),'.log']
  fid = fopen([Path.data,filename],'wt+')
for i in range(1, len(History.text)+1):
    count = fprintf(fid,'%s\n',History.text{i})
  fclose(fid)
  fm_text(13,[Path.data,filename])
  fm_print(['Log file written in ',Path.data,filename])

 case 2

  filename  = [fm_filenum('log'),'.log']
  fid = fopen([Path.data,filename],'wt+')
  value = get(Hdl.hist,'Value')
for i in range(1, len(value)+1):
    count = fprintf(fid,'%s\n',History.text{value(i)})
  fclose(fid)
  fm_text(13,[Path.data,filename])
  fm_print(['Log file written in ',Path.data,filename])

 case 3

  Hdl.hist = findobj(Fig.hist,'Tag','Listbox1')
  value = get(Hdl.hist,'Value')
  History.text(value) = []
  if isempty(History.text)
    History.text = {'    '}
  set(Hdl.hist,'String',History.text)
  set(Hdl.hist,'Value',min(len(History.text),max(value)+1))
  drawnow
  History.index = 1

 case 4

  Hdl.hist = gcbo
  if not isempty(History.text)
    set(gcbo,'String',History.text)

 case 5  #  font list

  set(Hdl.hist,prop,valu)
  if strcmp(prop,'FontName')

    tag = get(gcbo,'Tag')
    numero = str2num(tag(5:end))

    versione = version
    if strcmp(versione(1),'6')
      numtot = len(listfonts)
    else
      numtot = 3
    ntot = fix(numtot/25)+sign(rem(numtot,25))
    ncol = fix(numero/25)+sign(rem(numero,25))

    hdlp = get(gcbo,'Parent')
    for i = 1:ncol-1, hdlp = get(hdlp,'Parent'); end
for i in range(1, ntot+1):
      hdlc = get(hdlp,'Children')
      if i == ncol, hdlb = hdlc(end); end
      set(hdlc,'Checked','off')
      hdlp = hdlc(1)

  else
    hdlp = get(gcbo,'Parent')
    hdlc = get(hdlp,'Children')
    set(hdlc,'Checked','off')
  set(gcbo,'Checked','on')
  if ischar(valu)
    eval(['History.',prop,' = ''',valu,''';'])
  else
    eval(['History.',prop,' = [',num2str(valu),'];'])

 case 6 #  save settings

  fid = fopen([Path.psat,'history.ini'],'wt')
  s = fieldnames(History)
  slen = len(s)
  b = blanks(19)
for i in range(4, slen+1):
    a = eval(['History.',s{i}])
    campo = [s{i},b]
    campo = campo(1:19)
    if ischar(a)
      count = fprintf(fid,[campo,'''',a,''''])
    elseif len(a) > 1
      count = fprintf(fid,[campo,'[',num2str(a),']'])
    else
      count = fprintf(fid,[campo,num2str(a)])
    if i < slen
      count = fprintf(fid,'\n')
  count = fclose(fid)
  fm_print('Settings of command history window saved.')

 case 7   #  delete all

  set(Hdl.hist,'Value',1)
  History.text = {'    '}
  set(Hdl.hist,'String',History.text)
  drawnow
  History.index = 1

 case 8   #  find string

  testo = fm_input('Find:','History Search',1,{History.string})
  testo = testo{1}
  if isempty(testo)
    return
  if not strcmp(testo,History.string),
    History.index = 0
    History.string = testo
  fm_text(9)

 case 9   #  find next

  if isempty(History.string)
    fm_text(8)

for i in range(History.index+1, len(History.text)+1):
    if not isempty(findstr(History.text{i},History.string))
      set(Hdl.hist,'Value',i,'ListboxTop',max(i-5,1))
      drawnow
      History.index = i
      return
  if History.index != 0
    History.index = 0
    fm_text(9)
  else
    fm_print(['No match for text "',History.string,'".'],2)

 case 10

  hdlp = get(gcbo,'Parent')
  hdlc = get(hdlp,'Children')
  set(hdlc,'Checked','off')
  set(gcbo,'Checked','on')
  set(Hdl.hist,'Max',History.Max)

 case 11

  actcol = eval(['History.',prop])
  color = uisetcolor(actcol)
  if len(color) == 3  and  color != actcol
    eval(['History.',prop,' = [',num2str(color),'];'])
    hdlp = get(gcbo,'Parent')
    hdlc = get(hdlp,'Children')
    set(hdlc,'Checked','off')
    set(gcbo,'Checked','on')
    set(Hdl.hist,prop,color)

 case 12 #  set output to workspace

  History.workspace = not History.workspace
  if History.workspace,
    set(gcbo,'Checked','on')
  else
    set(gcbo,'Checked','off')

 case 13 #  view the selected file with the proper viewer

  if clpsat.init  and  not clpsat.viewrep
    return

  if strcmp(prop(1:2),'~/')
    prop = [getenv('HOME'),prop(2:end)]
  a5 = '';  a6 = 1
  a1 = strcmp(Settings.tviewer, '!cat ')
  a2 = strcmp(Settings.tviewer, '!type ')
  a3 = strcmp(Settings.tviewer, '!awk ''{print}'' ')
  a4 = strcmp(Settings.tviewer, '!gawk ''{print}'' ')
  if not (a1  or  a2  or  a3  or  a4)
    a5 = ' &'
    a6 = 0
  if a6
    print(['file: ''',prop,''''])
    print(' ')
  eval([Settings.tviewer,'"',prop,'"',a5])
  if a6
    print(blanks(3)')

 case 14 #  select output format

  if not ishandle(Fig.tviewer), return, end

  hdl1 = findobj(Fig.tviewer,'Tag','PushTXT')
  hdl2 = findobj(Fig.tviewer,'Tag','PushTEX')
  hdl3 = findobj(Fig.tviewer,'Tag','PushXLS')
  hdl4 = findobj(Fig.tviewer,'Tag','PushHTM')

  switch gcbo
  case hdl1
    set(hdl1,'Value',1)
    set(hdl2,'Value',0)
    set(hdl3,'Value',0)
    set(hdl4,'Value',0)
    Settings.export = 'txt'
  case hdl2
    set(hdl1,'Value',0)
    set(hdl2,'Value',1)
    set(hdl3,'Value',0)
    set(hdl4,'Value',0)
    Settings.export = 'tex'
  case hdl3
    set(hdl1,'Value',0)
    set(hdl2,'Value',0)
    set(hdl3,'Value',1)
    set(hdl4,'Value',0)
    Settings.export = 'xls'
  case hdl4
    set(hdl1,'Value',0)
    set(hdl2,'Value',0)
    set(hdl3,'Value',0)
    set(hdl4,'Value',1)
    Settings.export = 'html'

