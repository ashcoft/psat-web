# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_comp.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_comp(flag):

# FM_COMP define settings and operations of the GUI
#         for creating new components
#
# FM_COMP(FLAG)
#
#see also FM_MAKE FM_COMPONENT FM_BUILD
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    12-Feb-2003
#Update:    15-Sep-2003
#Version:   1.1.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Path Comp Fig
global Algeb Buses Initl Param Servc State

switch flag

 case 'copen'

  if not ishandle(Fig.comp),
    fm_component
    lasterr('')

# Structure initialization
    Algeb = struct('name',[],'n',0,'idx',[],'eq',[],'eqidx',[],'neq',0)
    Buses = struct('name',[],'n',0)
    State = struct('name',[],'n',0,'eq',[],'eqidx',[],'neq',0, ...
		   'init',[],'limit',[],'fn',[],'un',[],'time',[],'offset',[],'nodyn',[])
    Initl = struct('name',[],'n',0,'idx',[])
    Param = struct('name',[],'n',0,'descr',[],'type',[],'unit',[])
    Servc = struct('name',[],'n',0,'idx',[],'eq',[],'eqidx',[],'neq',0, ...
		   'init',[],'limit',[],'fn',[],'un',[],'type',[],'offset',[],'oldidx',[])

    Comp.init = 0
    Comp.descr = ''
    Comp.shunt = 1
    Comp.series = 0
  else
    figure(Fig.comp)

 case 'clist'

  a = dir([Path.build,'*.m'])
  b = sort({a.name}');
for i in range(1, len(b)+1):
    b{i} = strrep(b{i},'.m','')
  set(findobj(Fig.comp,'Tag','Listbox1'),'String',b)

 case 'cload'

  fm_make
  fm_open(Path.build,popupstr(findobj(Fig.comp,'Tag','Listbox1')),1)

 case 'cbuild'

  fm_open(Path.build,popupstr(findobj(Fig.comp,'Tag','Listbox1')),0)
  fm_build

 case 'cinstall'

  fm_open(Path.build,popupstr(findobj(Fig.comp,'Tag','Listbox1')),0)
  fm_install

 case 'cuninstall'

  fm_open(Path.build,popupstr(findobj(Fig.comp,'Tag','Listbox1')),0)
  fm_uninstall

 case 'cprop'

  fm_cset
  hdl = get(Fig.cset,'UserData')
  set(hdl(1),'String',Comp.name)      #  name
  set(hdl(2),'Value', Comp.init)      #  initialization
  set(hdl(3),'String',Comp.descr)     #  description
  if not isempty(Comp.name)
    set(hdl(4),'String',Comp.name)    #  name
  set(hdl(5),'Value',Comp.shunt)      #  shunt
  set(hdl(6),'Value',Comp.series)     #  series

 case 'cset'

  fm_cset
  hdl = get(Fig.cset,'UserData')

  Comp.name   = get(hdl(1),'String');  #  name
  Comp.init   = get(hdl(2),'Value');   #  initialization
  Comp.descr  = get(hdl(3),'String');  #  description
  Comp.shunt  = get(hdl(5),'Value');   #  shunt
  Comp.series = get(hdl(6),'Value');   #  series
  if not isempty(Comp.name),
    set(hdl(4),'String',Comp.name)
    hdl = get(Fig.make,'UserData')
    set(hdl(1),'String',Comp.name)

  if strcmp(get(gcbo,'String'),'Ok')
    close(Fig.cset)
    return

 case 'popen'

  if not Param.n, fm_print('No parameter is present.'), return, end
  fm_pset
  qualep = get(findobj(Fig.make,'Tag','ListboxParameter'),'Value')
  hdl = get(Fig.pset,'UserData')

  set(hdl(1),'Value',strmatch(Param.unit{qualep,1},get(hdl(1),'String'),'exact'))  #  units
  set(hdl(2),'Value',strmatch(Param.type{qualep,1},get(hdl(2),'String'),'exact'))  #  type
  set(hdl(3),'String',Param.descr{qualep,1})                               #  description
  set(hdl(4),'String',Param.name{qualep,1})                                #  variable name

 case 'pset'

  qualep = get(findobj(Fig.make,'Tag','ListboxParameter'),'Value')
  hdl = get(Fig.pset,'UserData')

  Param.unit{qualep,1} = popupstr(hdl(1));       #  units
  Param.type{qualep,1} = popupstr(hdl(2));       #  type
  descr = get(hdl(3),'String')
  if isempty(descr), descr = 'None'; end
  Param.descr{qualep,1} = descr;  #  description

  if strcmp(get(gcbo,'String'),'Ok'), close(Fig.pset); end

 case 'serv'

  nome = popupstr(gcbo)
  a = strmatch(nome,Servc.idx(end-2*Buses.n+1:end-Buses.n),'exact')
  b = strmatch(nome,Servc.idx(end-Buses.n+1:end),'exact')
  if isempty(a), a = 0; end
  if isempty(b), b = 0; end
  hdl = findobj(gcf,'Tag','PushbuttonSettServiceVar')
  if a  or  b
    set(hdl,'Enable','off')
  else
    set(hdl,'Enable','on')

 case 'sopen'

  if not Servc.n, fm_print('No service variable is present.'), return, end
  fm_sset
  nome = popupstr(findobj(Fig.make,'Tag','ListboxServiceVar'))
  qualep = strmatch(nome,Servc.eqidx,'exact')
  hdl = get(Fig.sset,'UserData')

  set(hdl(1),'String',{'None';[Servc.name{qualep,1},'_min'];'0'},'Value',1);  #  limit strings
  set(hdl(2),'String',{'None';[Servc.name{qualep,1},'_max'];'0'})

  set(hdl(1),'Value',strmatch(Servc.limit{qualep,2},get(hdl(1),'String'),'exact'))    #  min limit
  set(hdl(2),'Value',strmatch(Servc.limit{qualep,1},get(hdl(2),'String'),'exact'))    #  max limit
  set(hdl(3),'Value',strmatch(Servc.type{qualep,1},get(hdl(3),'String'),'exact'));    #  variable type
  set(hdl(4),'Value',strmatch(Servc.offset{qualep,1},get(hdl(4),'String'),'exact'));  #  offset
  set(hdl(5),'String',Servc.init{qualep,1},'UserData',Servc.init{qualep,1});  #  initial value
  set(hdl(6),'String',Servc.un{qualep,1});                                    #  matlab name
  set(hdl(7),'String',Servc.fn{qualep,1});                                    #  TeX name
  set(hdl(8),'String',Servc.name{qualep,1});                                  #  variable name

 case 'sset'

  nome = popupstr(findobj(Fig.make,'Tag','ListboxServiceVar'))
  qualep = strmatch(nome,Servc.eqidx,'exact')
  hdl = get(Fig.sset,'UserData')

  Servc.limit{qualep,2} = popupstr(hdl(1));       #  min limit
  Servc.limit{qualep,1} = popupstr(hdl(2));       #  max limit
  Servc.type{qualep,1} = popupstr(hdl(3));        #  variable type
  Servc.offset{qualep,1} = popupstr(hdl(4));      #  offset
  Servc.init{qualep,1} = get(hdl(5),'String');    #  initial value
  fname = get(hdl(7),'String')
  if isempty(fname)
    fname = Servc.name{qualep,1}
  Servc.fn{qualep,1} = fname;                     #  TeX name

  if strcmp(get(gcbo,'String'),'Ok')
    close(Fig.sset)

 case 'xopen'

  if not State.n, fm_print('No state variable is present.'), return, end
  fm_xset
  qualep = get(findobj(Fig.make,'Tag','ListboxState'),'Value')
  hdl = get(Fig.xset,'UserData')

  set(hdl(1),'String',{'None';[State.name{qualep,1},'_min'];'0'})             #  popup strings
  set(hdl(2),'String',{'None';[State.name{qualep,1},'_max'];'0'})
  set(hdl(3),'String',{'None',Param.name{strmatch('Time Constant',Param.type,'exact')}})

  set(hdl(1),'Value',strmatch(State.limit{qualep,2},get(hdl(1),'String'),'exact'))    #  min limit
  set(hdl(2),'Value',strmatch(State.limit{qualep,1},get(hdl(2),'String'),'exact'))    #  max limit
  set(hdl(3),'Value',strmatch(State.time{qualep,1},get(hdl(3),'String'),'exact'))     #  time constant
  set(hdl(4),'Value',strmatch(State.nodyn{qualep,1},get(hdl(4),'String'),'exact'))    #  allows no dynamic
  set(hdl(5),'Value',strmatch(State.offset{qualep,1},get(hdl(5),'String'),'exact'))   #  offset
  set(hdl(6),'String',State.name{qualep,1});                                  #  variable name
  set(hdl(7),'String',State.init{qualep,1});                                  #  initial value
  set(hdl(8),'String',State.un{qualep,1});                                    #  Matlab name
  set(hdl(9),'String',State.fn{qualep,1});                                    #  TeX value

 case 'xset'

  qualep = get(findobj(Fig.make,'Tag','ListboxState'),'Value')
  hdl = get(Fig.xset,'UserData')

  State.limit{qualep,2}  = popupstr(hdl(1));       #  min limit
  State.limit{qualep,1}  = popupstr(hdl(2));       #  max limit
  State.time{qualep,1}   = popupstr(hdl(3));       #  time constant
  State.nodyn{qualep,1}  = popupstr(hdl(4));       #  allow no dynamic
  State.offset{qualep,2} = popupstr(hdl(5));       #  offset
  State.init{qualep,1} = get(hdl(7),'String');     #  initial value
  fname = get(hdl(9),'String')
  if isempty(fname), fname = State.name{qualep,1}; end
  State.fn{qualep,1} = fname;                      #  TeX name

  hdl = get(Fig.make,'UserData')
  set(hdl(10),'String',fm_strjoin(State.eqidx,' = (',State.eq,')/',State.time)) #  reset time constants

  if strcmp(get(gcbo,'String'),'Ok'), close(Fig.xset); end

 case 'mdelxe'

  if State.n > 0
    hdl = findobj(gcf,'Tag','ListboxStateEquation')
    valore = get(hdl,'Value')
    State.eq{valore,1} = 'null'
    set(hdl,'String',fm_strjoin(State.eqidx,' = (',State.eq,')/',State.time))

 case 'maddxe'

  hdl = get(Fig.make,'UserData')
  espress = get(hdl(3),'String')
  valore = get(hdl(10),'Value')
  if not isempty(espress)
    State.eq{valore,1} = espress
    set(hdl(10),'String',fm_strjoin(State.eqidx,' = (',State.eq,')/',State.time))

 case 'maddae'

  hdl  = findobj(gcf,'Tag','EditTextEquation')
  espress = get(hdl,'String')
  hdl = findobj(gcf,'Tag','ListboxAlgebraicEquation')
  valore = get(hdl,'Value')
  if not isempty(espress)
    Algeb.eq{valore,1} = espress
    set(hdl,'String',fm_strjoin(Algeb.eqidx,'=',Algeb.eq))

 case 'mdelae'

  hdl = findobj(gcf,'Tag','ListboxAlgebraicEquation')
  valore = get(hdl,'Value')
  Algeb.eq{valore,1} = 'null'
  set(hdl,'String',fm_strjoin(Algeb.eqidx,'=',Algeb.eq))

 case 'maddse'

  hdl  = findobj(gcf,'Tag','EditTextEquation')
  espress = get(hdl,'String')
  hdl = findobj(gcf,'Tag','ListboxServiceEquation')
  valore = get(hdl,'Value')
  if not isempty(espress)
    Servc.eq{valore,1} = espress
    set(hdl,'String',fm_strjoin(Servc.eqidx,'=',Servc.eq))

 case 'mdelse'

  hdl = findobj(gcf,'Tag','ListboxServiceEquation')
  valore = get(hdl,'Value')
  Servc.eq{valore,1} = 'null'
  set(hdl,'String',fm_strjoin(Servc.eqidx,'=',Servc.eq))

 case 'mlistae'

  if strcmp(get(Fig.make,'SelectionType'),'open')
    fm_comp mcallae

 case 'mlistse'

  if strcmp(get(Fig.make,'SelectionType'),'open')
    fm_comp mcallse

 case 'mmenua'

  if iscell(Algeb.idx)

    hdl = findobj(gcf,'Tag','PopupMenuAlgebraic')
    numero = get(hdl,'Value')
    stringa = get(hdl,'String')
    if strcmp(stringa,' ')
      return
    else
      nome = Algeb.idx{numero,1}

    indice = 1
for i in range(1, Algeb.n+1):
      addalgebraic = strncmp(nome,Algeb.name{i},len(nome))
      if addalgebraic == 1  and  (nome(1) == 'V'  or  nome(1) == 't')
	fm_print(['Variable "',nome,'" was already set.'])
	return
      indice = indice + addalgebraic
    if not (nome(1) == 'V'  or  nome(1) == 'theta')
      nome = [nome, int2str(indice)]

    hdl = findobj(gcf,'Tag','EditTextVariable')
    set(hdl,'String',nome)
    [Algeb.name, Algeb.n] = fm_add(Algeb.name, Algeb.n, ...
				   'ListboxAlgebraic', 'EditTextVariable')


 case 'mmenus'

  hdl = findobj(gcf,'Tag','PopupMenuService')
  numero = get(hdl,'Value')
  stringa = get(hdl,'String')
  if strcmp(stringa,' ')
    return
  else
    nome = Servc.idx{numero,1}
  if strmatch(nome,Servc.name,'exact')
    fm_print('Variable already set.',2)
    return
  if nome(1)!='P'  and  nome(1)!='Q'
    nome = [nome,num2str(len(strmatch(nome,Servc.name))+1)]

  hdl = findobj(gcf,'Tag','EditTextVariable')
  set(hdl,'String',nome)
  [Servc.name, Servc.n] = fm_add(Servc.name, Servc.n,'ListboxServiceVar','EditTextVariable')
  fm_comp serv

 case 'mlistxe'

  if strcmp(get(Fig.make,'SelectionType'),'open'), fm_comp mcallxe, end

 case 'mcallxe'

  if not isempty(State.eq)
    hdl = get(Fig.make,'UserData')
    valore = get(hdl(10), 'Value')
    A = State.eq{valore,1}
    if strcmp(A,'null'); A = ''; end
    set(hdl(3),'String',A)

 case 'mcallae'

  hdl =  findobj(gcf,'Tag','ListboxAlgebraicEquation')
  valore = get(hdl, 'Value')
  A = Algeb.eq{valore,1}
  if strcmp(A,'null'); A = ''; end
  hdl = findobj(gcf,'Tag','EditTextEquation')
  set(hdl,'String',A)

 case 'mcallse'

  hdl =  findobj(gcf,'Tag','ListboxServiceEquation')
  valore = get(hdl, 'Value')
  A = Servc.eq{valore,1}
  if strcmp(A,'null'); A = ''; end
  hdl = findobj(gcf,'Tag','EditTextEquation')
  set(hdl,'String',A)

 case 'mmenui'

  if iscell(Initl.idx)

    hdl = findobj(gcf,'Tag','PopupMenuInit')
    numero = get(hdl,'Value')
    stringa = get(hdl,'String')
    if strcmp(stringa,' '), return, else, nome = Initl.idx{numero,1}; end
for i in range(1, Initl.n+1):
      addinitial = strncmp(nome,Initl.name{i},len(nome))
      if addinitial == 1
	fm_print(['Variable "',nome,'" was already set'])
	return

    hdl = findobj(gcf,'Tag','EditTextVariable')
    set(hdl,'String',nome)
    [Initl.name, Initl.n] = fm_add(Initl.name, Initl.n, ...
				   'ListboxInitial', 'EditTextVariable')

 case 'name'

  nome = lower(get(gcbo,'String'))
  if isvarname(nome)
    set(gcbo,'String',nome)
  else
    set(gcbo,'String',Comp.name)
    fm_print(['The string "',nome,'" is not a valid Matlab variable.'],2)

