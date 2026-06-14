# Module: psat.gui.fm_plot
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_plot(flag):

# FM_PLOT plot results of Continuation Power Flow,
#         Optimal Power Flow and Time Domain
#         Simulations.
#
# FM_PLOT(FLAG)
#    FLAG  0 -> create variable list
#          1 -> plot selected variables
#          2 -> save graph
#          3 -> set layout
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    25-Feb-2003
#Update:    26-Jan-2005
#Version:   1.0.2
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global DAE Bus Syn Settings Fig Snapshot Hdl CPF Theme
global Varout Varname Path File OPF Line Mass SSR Pmu

#hdls = get(Fig.plot, 'Children')
#display(hdls)

hdlfig = findobj(Fig.plot, 'Tag','Axes1')
hdlfig2 = findobj(Fig.plot, 'Tag','Axes2')
Hdl_grid = findobj(Fig.plot,'Tag','Checkbox1')
Hdl_legend = findobj(Fig.plot,'Tag','Checkbox2')
Hdl_listvar = findobj(Fig.plot,'Tag','Listbox1')
Hdl_listplot = findobj(Fig.plot,'Tag','Listbox2')
Hdl_tipoplot = findobj(Fig.plot,'Tag','PopupMenu1')
Hdl_angref = findobj(Fig.plot,'Tag','PopupMenu2')
Hdl_snap = findobj(Fig.plot,'Tag','Radiobutton1')
hdl_zoom1 = findobj(Fig.plot,'Tag','Pushbutton12')
hdl_zoom2 = findobj(Fig.plot,'Tag','Pushbutton11')
hdl_zoom3 = findobj(Fig.plot,'Tag','Pushbutton4')
hdl_x = findobj(Fig.plot,'Tag','Pushbutton9')
hdl_y = findobj(Fig.plot,'Tag','Pushbutton5')
hdl_xy = findobj(Fig.plot,'Tag','Pushbutton10')

switch flag
 case 'exporttext',  #  output data as plain text file
  flag = 'plotvars'
  out_matlab = 0
  out_mtv = 0
  out_text = 1
 case 'exportmtv',  #  output data as plain text file
  flag = 'plotvars'
  out_matlab = 0
  out_mtv = 1
  out_text = 0
 case 'exportscript',  #  output data as plain text file
  flag = 'plotvars'
  out_matlab = 1
  out_mtv = 0
  out_text = 0
 otherwise
  out_matlab = 0
  out_mtv = 0
  out_text = 0

switch flag

 case 'initlist'

  if not strcmp(get(Fig.plot,'UserData'),File.modify)
    set(Hdl_listvar, ...
        'String',enum(Varname.uvars(Varout.idx)), ...
        'Value',1)
    if Settings.hostver < 8.04
      set(Fig.plot,'DefaultAxesColorOrder',Settings.color, ...
                   'DefaultAxesLineStyle','-')
  set(Fig.plot,'UserData',File.modify)
  Varname.pos = 1

 case 'initxlabel'

  first = strrep(Settings.xlabel,'\','')
  hdl = findobj(Fig.plot,'Tag','Listbox1')
  stringa = get(hdl,'String')
  hdl = findobj(Fig.plot,'Tag','PopupMenu3')
  if not isempty(stringa)
    set(hdl,'String',[{first}; stringa],'Enable','on','Value',1)

 case 'plotvars'

  if isempty(Varout.t)
    fm_print('Plotting Utilities: No data available for plotting.')
    return

  if isempty(Varname.pos)
    fm_print('Plotting Utilities: Select variables to be plotted.')
    return

  nB = Bus.n
  nD = DAE.n

  Value = get(Hdl_listvar,'Value')
  if isempty(Value), return, end
  hdlfig = findobj(Fig.plot, 'Tag', 'Axes1')
  AxesFont   = get(hdlfig,'FontName')
#AxesColor  = get(hdlfig,'Color');
#if ~length(AxesColor)
  AxesColor = [1, 1, 1]
#end
  AxesWeight = get(hdlfig,'FontWeight')
  AxesAngle  = get(hdlfig,'FontAngle')
  AxesSize   = get(hdlfig,'FontSize')
  AxesUnits  = get(hdlfig,'FontUnits')

  plot_snap = get(Hdl_snap,'Value')
  snap_idx = np.zeros((len(Snapshot),1))
  if plot_snap  and  not OPF.init
    for i = 1:len(Snapshot)
      a = find(Varout.t == Snapshot(i).time)
      if isempty(a)
        fm_print('Plotting utilities: Snapshots do not match current simulation data',2)
        Hdl_rad1 = findobj(gcf,'Tag','Radiobutton1')
        set(Hdl_rad1,'Value',0)
        plot_snap = 0
        break
      else
        snap_idx(i) = a

  legenda = Varname.fvars(Varout.idx(Value(Varname.pos)))
  leg_value = get(Hdl_legend,'Value')

  hdlab = findobj(Fig.plot,'Tag','PopupMenu3')
  AbValue = get(hdlab,'Value')

  Y = Varout.vars(:,Value)
  if isempty(Y), return, end

# set angle unit
  if Settings.usedegree
    kdx = get_angle_idx(Value)
    Y(:,kdx) = 180*Y(:,kdx)/np.pi

# set rotor speed unit and values
  if Settings.usehertz  or  Settings.userelspeed
    kdx = get_rotor_idx(Value)
    if Settings.userelspeed
      Y(:,kdx) = Y(:,kdx)-1
    if Settings.usehertz
      Y(:,kdx) = Settings.freq*Y(:,kdx)

# set reference angle
  if not OPF.init
    ang_idx = get(Hdl_angref,'Value')-1
    if not ang_idx
      angolo = np.zeros((len(Varout.t),1))
    else
      ref_idx = get(Hdl_angref,'UserData')
      ang_ref = ref_idx(ang_idx)
      angolo = Varout.vars(:,ang_ref)
for i in range(1, len(Value)+1):
      kk = Varout.idx(Value(i))
      if isdelta(Syn,kk)  or  isdelta(Mass,kk)  or  isdelta(SSR,kk)  or  isdelta(Pmu,kk)
        Y(:,i) = Y(:,i) - angolo
      elseif kk >= nD+1  and  kk <= nD+nB
        Y(:,i) = Y(:,i) - angolo

  hdlnorm = findobj(Fig.plot,'Tag','NormSij')
  if strcmp(get(hdlnorm,'Checked'),'on')
for i in range(1, len(Value)+1):
      kk = Varout.idx(Value(i))
      Y(:,i) = isflow(Line,Y(:,i),kk)

  if AbValue == 1
    X = Varout.t
  else
    X = Varout.vars(:,AbValue-1)
# set angle unit
    check = get_angle_idx(AbValue-1)
    if Settings.usedegree  and  not isempty(check)
      X = 180*X/np.pi
# set rotor speed unit and values
    if Settings.usehertz  or  Settings.userelspeed
      check = get_rotor_idx(AbValue-1)
      if Settings.userelspeed  and  check
        X = X-1
      if Settings.usehertz  and  check
        X = Settings.freq*X

  tipoplot = get(Hdl_tipoplot,'Value')

  if out_text
    plainfile = fm_filenum('txt')
    fid = fopen([Path.data,plainfile,'.txt'],'wt')
    if fid == -1
      fm_print('Cannot open file. Data not saved.')
      return
    fprintf(fid,'C Legend:\n')
    fprintf(fid,'C %s,  ',Settings.xlabel)
    for i = 1:size(Y,2)
      fprintf(fid,'%s,  ',legenda{i})
    fprintf(fid,'\nC Data:\n')
    fprintf(fid,[repmat('%8.5f  ',1,1+size(Y,2)),'\n'],[X,Y]');
    fclose(fid)
    fm_print(['Data exported to plain text file "',plainfile,'.txt"'])

  if out_mtv
    plainfile = fm_filenum('mtv')
    fid = fopen([Path.data,plainfile,'.mtv'],'wt')
    if fid == -1
      fm_print('Cannot open file. Data not saved.')
      return
#fprintf(fid,'$ DATA=CURVE2D\n');
    fprintf(fid,'%% xlabel = "%s"\n',Settings.xlabel)
    if min(X) < max(X)
      fprintf(fid,'%% xmin = %8.5f\n',min(X))
      fprintf(fid,'%% xmax = %8.5f\n',max(X))
    fprintf(fid,'\n')
    if tipoplot == 3  or  tipoplot == 6
      fm_print('MTV format does not support numbered plots.')

    for i = 1:size(Y,2)
      labelmtv = strrep(legenda{i},'{','')
      labelmtv = strrep(labelmtv,'}','')
      labelmtv = strrep(labelmtv,'_',' ')
      labelmtv = strrep(labelmtv,'\','')
      fprintf(fid,'%% linelabel="%s"\n',labelmtv)
      switch tipoplot
       case 2
        linetype = rem(i-1,10)+1
        linecolor = 1
        markertype = 0
        markercolor = 1
       case 4
        linetype = 1
        linecolor = 1
        markertype = rem(i-1,13)+1
        markercolor = 1
       case 5
        linetype = 1
        linecolor = rem(i-1,10)+1
        markertype = rem(i-1,13)+1
        markercolor = linecolor
       otherwise
        linetype = 1
        linecolor = rem(i-1,10)+1
        markertype = 0
        markercolor = 1
      fprintf(fid,'%% linetype=%d linecolor=%d markertype=%d markercolor=%d\n', ...
              linetype,linecolor,markertype,markercolor)
      fprintf(fid,'%8.5f %8.5f\n',[X,Y(:,i)]');
      fprintf(fid,'\n')

    fclose(fid)
    fm_print(['Data exported to MTV plot file "',plainfile,'.mtv"'])

  if out_matlab
    plainfile = fm_filenum('m')
    fid = fopen([Path.data,plainfile,'.m'],'wt')
    if fid == -1
      fm_print('Cannot open file. Data not saved.')
      return
    fprintf(fid,'x_label = ''%s'';\n',Settings.xlabel)
    fprintf(fid,'\nvar_legend = {')
    for i = 1:size(Y,2)-1
      fprintf(fid,'''%s'', ',legenda{i})
    fprintf(fid,'''%s''};\n',legenda{end})
    fprintf(fid,'\noutput_data = [ ...\n')
    fprintf(fid,[repmat('%8.5f  ',1,1+size(Y,2)),';\n'], ...
            [X(1:end-1),Y(1:end-1,:)]');
    fprintf(fid,[repmat('%8.5f  ',1,1+size(Y,2)),'];\n'], ...
            [X(end),Y(end,:)]');
    fclose(fid)
    fm_print(['Data exported to plain text file "',plainfile,'.m"'])

  set(Fig.plot,'CurrentAxes',hdlfig)
  plot(X,Y(:,Varname.pos))
  set(hdlfig, 'Tag', 'Axes1')

  if AbValue == 1
    xlabel(Settings.xlabel)
  else
    xlabel(Varname.fvars{Varout.idx(AbValue-1)})
  if min(X) < max(X)
    set(hdlfig,'XLim',[min(X),max(X)])

#legend
  if leg_value == 1  or  Settings.hostver >= 7
    if Settings.hostver >= 8.04
        hleg = legend(legenda, 'Location', 'northeast')
    else
        hleg = legend(legenda, 0)
    Hdl.legend = hleg
    set(hleg,'Color',AxesColor)
    hchild = get(hleg,'Child')
    if ishandle(hchild)
      set(hchild(end), ...
          'FontName',AxesFont, ...
          'FontWeight',AxesWeight, ...
          'FontAngle',AxesAngle)

  hdlfig = findobj(Fig.plot, 'Tag', 'Axes1')
# display(hdlfig)
# axes(hdlfig)

  if tipoplot == 3  or  tipoplot == 6

    [quanti,tanti] = size(Y)
    colori = get(gcf,'DefaultAxesColorOrder')

for i in range(1, tanti+1):
      if plot_snap
        sequenza = snap_idx
      else
        tmin = min(X)
        tmax = max(X)
        deltat = (tmax-tmin)/5
        tmin = tmin + i*(tmax-tmin)/43
        seqt = tmin:deltat:tmax
        for j = 1:len(seqt),
          [valt, sequenza(j)] = min(abs(X-seqt(j)))
      hdl = text(X(sequenza),Y(sequenza,i),num2str(Varname.pos(i)))
      if tipoplot == 6,
        set(hdl,'Color',colori(rem(i-1,7)+1,:))

    if leg_value == 1  or  Settings.hostver >= 7
      hdl = findobj(Fig.plot,'Tag','legend')
#get(hdl)
      oldh = gca
      set(gca,'HandleVisibility','off')
      set(hdl,'Interruptible','on')
      h = findobj(hdl,'Type','line')
#get(hdl)
for i in range(1, tanti+1):
        j = i*2
        xdata = get(h(j),'XData')
        ydata = get(h(j),'YData')
        htext = text((xdata(2)-xdata(1))/2,ydata(1), ...
                     int2str(tanti-i+1))
        set(htext,'Color',get(h(j),'Color'))
      set(oldh,'HandleVisibility','on')
      set(Fig.plot,'CurrentAxes',oldh)

  elseif tipoplot == 4  or  tipoplot == 5

    [quanti,tanti] = size(Y)
    hold on
    simboli = {'o';'s';'d';'v';'^';'<';'>';'x'}
    colori = get(Fig.plot,'DefaultAxesColorOrder')

for i in range(1, tanti+1):
      if plot_snap
        sequenza = snap_idx
        if tanti == 1  and  CPF.init
          y1 = get(hdlfig,'YLim')
          yoff = 0.05*(y1(2)-y1(1))
for hh in range(1, len(sequenza)+1):
            text(X(sequenza(hh)), ...
                 Y(sequenza(hh),Varname.pos(i))+yoff, ...
                 Snapshot(hh).name)
      else
        tmin = min(X)
        tmax = max(X)
        deltat = (tmax-tmin)/5
        tmin = tmin + i*(tmax-tmin)/43
        seqt = tmin:deltat:tmax
        for j = 1:len(seqt),
          [valt, sequenza(j)] = min(abs(X-seqt(j)))
      set(hdlfig,'LineStyle',simboli{rem(i-1,8)+1}, 'Tag', 'Axes1')
      hmarker = plot(X(sequenza),Y(sequenza,Varname.pos(i)))
      set(hmarker,'MarkerSize',7,'MarkerFaceColor',AxesColor)
      if tipoplot == 5,
        set(hmarker,'Color',colori(rem(i-1,7)+1,:))
    hold off

    if leg_value == 1  or  Settings.hostver >= 7
      hdl = findobj(Fig.plot,'Tag','legend')
      set(Fig.plot,'CurrentAxes',hdl)
      h = findobj(hdl,'Type','line')
for i in range(1, tanti+1):
        j = i*2
        xdata = get(h(j),'XData')
        ydata = get(h(j),'YData')
        set(hdl,'LineStyle',simboli{rem(tanti-i,8)+1})
        if Settings.hostver >= 7
          hmarker = plot(hdl,(xdata(2)-xdata(1))/1.2,ydata(1))
        else
          hmarker = plot((xdata(2)-xdata(1))/1.2,ydata(1))
        set(hmarker,'MarkerSize',7, ...
                    'Color',get(h(j),'Color'), ...
                    'MarkerFaceColor',AxesColor)
      set(Fig.plot,'CurrentAxes',hdlfig)


  if get(Hdl_grid,'Value'); grid on; end
  if not get(Hdl_legend,'Value')  and  Settings.hostver >= 7  and  Settings.hostver < 8.04
    legend(findobj(Fig.plot,'Tag','Axes1'),'hide')
  set(get(hdlfig,'XLabel'), ...
      'FontName',AxesFont, ...
      'FontWeight',AxesWeight, ...
      'FontAngle',AxesAngle, ...
      'FontSize',AxesSize, ...
      'FontUnits',AxesUnits)
  set(hdlfig, ...
      'FontName',AxesFont, ...
      'Color',AxesColor, ...
      'FontWeight',AxesWeight, ...
      'FontAngle',AxesAngle, ...
      'FontSize',AxesSize, ...
      'FontUnits',AxesUnits, ...
      'Tag','Axes1')

  if ishandle(Fig.line), fm_plot('createlinelist'), end
  if get(hdl_x, 'Value'), fm_plot('axesx'), end
  if get(hdl_y, 'Value'), fm_plot('axesy'), end
  if get(hdl_xy,'Value'), fm_plot('axesxy'), end
  fm_plot plotvlims
  fm_plot plotslims
  set(hdlfig,'Position',[0.09 0.4050 0.4754 0.5000], 'Tag', 'Axes1')

#display('ciao')
#display(hdlfig)

 case 'export' #  export the figure to file

  tag = get(gcbo,'Tag')
  axs_pos = get(Hdl.axesplot,'Position')
  fig_pos = get(Fig.plot,'Position')
  pap_pos = get(Fig.plot,'PaperPosition')
  pap_siz = get(Fig.plot,'PaperSize')

  leg_value = get(Hdl_legend,'Value')
  if leg_value
    pos_leg = get(Hdl.legend,'Position')

  shrink = 0.8; #  axes scale factor

  set(Hdl.axesplot,'Position',[0.13 0.11 0.855 0.875])
  set(Fig.plot,'Position',[fig_pos(1), fig_pos(2), ...
                      fig_pos(3)*shrink, fig_pos(4)*shrink])
  if leg_value
    pos_leg2(1) = 0.13 + 0.855*(pos_leg(1) - axs_pos(1))/axs_pos(3)
    pos_leg2(2) = 0.11 + 0.875*(pos_leg(2) - axs_pos(2))/axs_pos(4)
    pos_leg2(3) = pos_leg(3)*0.855/axs_pos(3)
    pos_leg2(4) = pos_leg(4)*0.875/axs_pos(4)
    set(Hdl.legend,'Position',pos_leg2)

    if pos_leg2(1)+pos_leg2(3) > 0.985
      Resize = (pos_leg2(1)+pos_leg2(3))/0.985
      fig_pos2 = [0.13 0.11 0.855 0.875]
      fig_pos2(3) = fig_pos2(3)/Resize
      fig_pos2(1) = fig_pos2(1)/Resize
      pos_leg2(3) = pos_leg2(3)/Resize
      pos_leg2(1) = pos_leg2(1)/Resize
      set(Hdl.axesplot,'Position',fig_pos2)
      set(Hdl.legend,'Position',pos_leg2)

  if Settings.hostver > 5.03,
    set(Fig.plot,'PaperSize',[pap_siz(1)*shrink, pap_siz(2)*shrink])
  ppos(3) = pap_pos(3)*shrink
  ppos(4) = pap_pos(4)*shrink
  ppos(1) = (pap_siz(1)-ppos(3))/2
  ppos(2) = (pap_siz(2)-ppos(4))/2
  set(Fig.plot,'PaperPosition',ppos)

  ax2_pos = get(Hdl.axeslogo,'Position')
  set(Hdl.axeslogo,'Position',[10 10 0.2 0.2])

  Hdl_all = get(Fig.plot,'Children')
  idx = find(Hdl_all==Hdl.axesplot)
  if idx, Hdl_all(idx) = []; end
  idx = find(Hdl_all==Hdl.axeslogo)
  if idx, Hdl_all(idx) = []; end
  if leg_value,
    idx = find(Hdl_all==Hdl.legend)
    if idx, Hdl_all(idx) = []; end

  set(Hdl_all,'Visible','off')

  lastwarn('')
  switch tag
   case 'PushEPS'
    nomefile = fm_filenum('eps')
    print(Fig.plot,'-depsc',[Path.data,nomefile])
    set(hdlfig,'Position',axs_pos)
    set(hdlfig2,'Position',ax2_pos)
    set(Fig.plot,'Position',fig_pos)
    set(Fig.plot,'PaperPosition',pap_pos)
    if Settings.hostver > 5.03,
      set(Fig.plot,'PaperSize',pap_siz)
    set(Hdl_all,'Visible','on')
    if leg_value
      set(Hdl.legend,'Position',pos_leg)
   case 'PushMeta'
    print(Fig.plot,'-dmeta')
    set(hdlfig,'Position',axs_pos)
    set(hdlfig2,'Position',ax2_pos)
    set(Fig.plot,'Position',fig_pos)
    set(Fig.plot,'PaperPosition',pap_pos)
    if Settings.hostver > 5.03,
      set(Fig.plot,'PaperSize',pap_siz)
    set(Hdl_all,'Visible','on')
    if leg_value
      set(Hdl.legend,'Position',pos_leg)
   case 'PushFig'
    figplot = Fig.plot
    Fig.plot = -1
    try
      figpos = get(0,'factoryFigurePosition')
      axspos = get(0,'factoryAxesPosition')
      figunit = get(0,'factoryFigureUnits')
      axsunit = get(0,'factoryAxesUnits')
    catch
      figpos = [100 100 660 520]
      axspos = [0.1300 0.1100 0.7750 0.8150]
      figunit = 'pixels'
      axsunit = 'normalized'
    set(figplot, ...
        'Units',figunit, ...
        'Position',figpos, ...
        'Menubar','figure', ...
        'Name','', ...
        'NumberTitle','on', ...
        'CreateFcn','', ...
        'DeleteFcn','', ...
        'UserData',[], ...
        'FileName','')
    set(Hdl.axesplot,'Color',[1 1 1],'Units',axsunit,'Position',axspos)
    if leg_value
      set(Hdl.legend,'Color',[1 1 1])
    delete(Hdl_all)
    delete(hdlfig2)
    fm_plotfig
    figure(figplot)
  if not isempty(lastwarn)  and  not strcmp(lastwarn,'File not found or permission denied')
    fm_print(lastwarn,2),

 case 'plottypes'

  tipoplot = get(Hdl_tipoplot,'Value')

  if Settings.hostver < 8.04
    switch tipoplot
     case 1,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',Settings.color, ...
          'DefaultAxesLineStyleOrder','-')
     case 2,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',[ 0 0 0 ], ...
          'DefaultAxesLineStyleOrder','-|-.|--|:')
     case 3,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',[ 0 0 0 ], ...
          'DefaultAxesLineStyleOrder','-')
     case 4,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',[ 0 0 0 ], ...
          'DefaultAxesLineStyleOrder','-')
     otherwise,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',Settings.color, ...
          'DefaultAxesLineStyleOrder','-')
  else
    switch tipoplot
     case 1,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',Settings.color, ...
          'DefaultAxesLineStyleOrder','-')
     otherwise,
      set(Fig.plot, ...
          'DefaultAxesColorOrder',[ 0 0 0 ], ...
          'DefaultAxesLineStyleOrder','-|-.|--|:')

  fm_plot('plotvars')

 case 'editvarname'

  value =  get(Hdl_listplot,'Value')
  if not isempty(get(Hdl_listplot,'String'))
    valori = get(Hdl_listvar,'Value')
    val = valori(Varname.pos(value))
    stringa = Varname.fvars(Varname.idx)
    nomeattuale = popupstr(Hdl_listplot)
    idx = findstr(nomeattuale,']')
    nomeattuale = nomeattuale(idx+2:end)
    nomenuovo = fm_input('Input Formatted Text:', ...
                         'Legend Name',1,{stringa{val}})
    if isempty(nomenuovo),
      return,
    Varname.fvars{Varname.idx(val)} = nomenuovo{1}
    set(Fig.plot,'UserData',stringa)
    fm_print(['Formatted text of variable "', ...
             nomeattuale,'" has been changed in "', ...
             nomenuovo{1},'"'])
  else
    fm_print('No variable selected')

 case 'zoomy'

  zoom yon
  set(Fig.plot,'WindowButtonMotionFcn','fm_plot motion')
  set(hdl_zoom1,'Value',0)
  set(hdl_zoom2,'Value',0)
  if get(hdl_zoom3,'Value')
    Settings.zoom = 'zoom yon'
  else
    Settings.zoom = ''
    zoom off

 case 'axesy'

  if get(hdl_x,'Value')
    set(hdl_x,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','x axis'))
  if get(hdl_xy,'Value')
    set(hdl_xy,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','x axis'))
    delete(findobj(allchild(hdlfig),'UserData','y axis'))

  value = get(gcbo,'Value')
  if value
    ylim = get(hdlfig,'YLim')
    hold on
    h = plot([0 0],[ylim(1), ylim(2)],'k:')
    set(h,'UserData','y axis')
    hold off
  else
    hdl_child = allchild(hdlfig)
    delete(findobj(hdl_child,'UserData','y axis'))
  if ishandle(Fig.line), fm_plot('createlinelist'), end

 case 'axescolor'

  currentColor = get(hdlfig,'Color')
  c = uisetcolor(currentColor)
  if not isequal(c,currentColor)
    set(hdlfig,'Color',c)
    hdl_line = findobj(allchild(hdlfig),'Type','line')
    set(hdl_line,'MarkerFaceColor',c)
    hlegend = findobj(Fig.plot,'Tag','legend')
    set(hlegend,'Color',c)

 case 'axesx'

  if get(hdl_y,'Value')
    set(hdl_y,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','y axis'))
  if get(hdl_xy,'Value')
    set(hdl_xy,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','y axis'))
    delete(findobj(allchild(hdlfig),'UserData','x axis'))

  value = get(gcbo,'Value')
  if value
    xlim = get(hdlfig,'XLim')
    hold on
    h = plot([xlim(1), xlim(2)], [0, 0],'k:')
    set(h,'UserData','x axis')
    hold off
  else
    hdl_child = allchild(hdlfig)
    delete(findobj(hdl_child,'UserData','x axis'))
  if ishandle(Fig.line), fm_plot('createlinelist'), end

 case 'axesxy'

  if get(hdl_x,'Value')
    set(hdl_x,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','x axis'))
  if get(hdl_y,'Value')
    set(hdl_y,'Value',0)
    delete(findobj(allchild(hdlfig),'UserData','y axis'))

  value = get(gcbo,'Value')
  if value
    xlim = get(hdlfig,'XLim')
    ylim = get(hdlfig,'YLim')
    hold on
    h = plot([xlim(1), xlim(2)], [0, 0],'k:')
    set(h,'UserData','x axis')
    h = plot([0, 0],[ylim(1), ylim(2)],'k:')
    set(h,'UserData','y axis')
    hold off
  else
    hdl_child = allchild(hdlfig)
    try
      delete(findobj(hdl_child,'UserData','x axis'))
    catch
# nothing to do
    try
      delete(findobj(hdl_child,'UserData','y axis'))
    catch
# nothing to do
  if ishandle(Fig.line), fm_plot('createlinelist'), end

 case 'zoomx'

  zoom xon
  set(Fig.plot,'WindowButtonMotionFcn','fm_plot motion')
  set(hdl_zoom1,'Value',0)
  set(hdl_zoom3,'Value',0)
  if get(hdl_zoom2,'Value')
    Settings.zoom = 'zoom xon'
  else
    Settings.zoom = ''
    zoom off

 case 'zoomxy'

  zoom on
  set(Fig.plot,'WindowButtonMotionFcn','fm_plot motion')
  set(hdl_zoom2,'Value',0)
  set(hdl_zoom3,'Value',0)
  if get(hdl_zoom1,'Value')
    Settings.zoom = 'zoom on'
  else
    Settings.zoom = ''
    zoom off

 case 'moveup'

  value = get(Hdl_listplot,'Value')
  NameString = get(Hdl_listplot,'String')
  Value = 1:len(NameString)

  if value > 1
    dummy = Varname.pos(value)
    Varname.pos(value) = Varname.pos(value-1)
    Varname.pos(value-1) = dummy
    dummy = Value(value)
    Value(value) = Value(value-1)
    Value(value-1) = dummy
    set(Hdl_listplot, ...
        'String',NameString(Value), ...
        'Value',value-1)

 case 'movedown'

  value = get(Hdl_listplot,'Value')
  NameString = get(Hdl_listplot,'String')
  Value = 1:len(NameString)

  if value < len(Varname.pos)  and  not isempty(NameString)
    dummy = Varname.pos(value)
    Varname.pos(value) = Varname.pos(value+1)
    Varname.pos(value+1) = dummy
    dummy = Value(value)
    Value(value) = Value(value+1)
    Value(value+1) = dummy
    set(Hdl_listplot, ...
        'String',NameString(Value), ...
        'Value',value+1)

 case 'togglegrid'

  if get(gcbo,'Value')
    grid on
  else
    grid off

 case 'togglelegend'

  if Settings.hostver >= 8.04
# axes(findobj(Fig.plot, 'Tag', 'Axes1'))
    legend toggle
  elseif Settings.hostver >= 7
    legend(findobj(Fig.plot,'Tag','Axes1'),'toggle')
  else
    onoff = {'off','on'}
    if strcmp(get(gcbo,'Tag'),'PushLegend')
      set(Hdl_legend,'Value',not get(Hdl_legend,'Value'))
      set(gcbo,'Checked',onoff{get(Hdl_legend,'Value')+1})
      value = get(Hdl_legend,'Value')
    else
      hdl = findobj(Fig.plot,'Tag','PushLegend')
      set(hdl,'Checked',onoff{get(gcbo,'Value')+1})
      value = get(gcbo,'Value')

    if value
      fm_plot('plotvars')
    else
      legend off

 case 'listvars'

  Value = get(Hdl_listvar,'Value')
  if isempty(Value), return, end
  NameString = get(Hdl_listvar,'String')
  if isempty(NameString), return, end
  set(Hdl_listplot,'String',NameString(Value))
  set(Hdl_listplot,'Value',1)
  Varname.pos = 1:len(Value)
  if strcmp(get(Fig.plot,'SelectionType'),'open'),
    fm_plot('plotvars')

 case 'listlines'

  hdl = findobj(Fig.line,'Tag','Listbox1')
  Value = get(hdl,'Value')
  hdl_line = get(Fig.line,'UserData')
  hdl_line = hdl_line(end:-1:1)
  fm_linedlg(hdl_line(Value))

 case 'createlinelist'

  hdl_line = findobj(allchild(hdlfig),'Type','line')
  variabili = get(Hdl_listplot,'String')
  set(Fig.line,'UserData',hdl_line)
  hdl_list = findobj(Fig.line,'Tag','Listbox1')
  line_string = cell(len(hdl_line),1)
  hdl_line = hdl_line(end:-1:1)
for i in range(1, len(hdl_line)+1):
    if strcmp(get(hdl_line(i),'UserData'),'x axis')
      line_string{i,1} = ['x axis ',fvar(i,4)]
    elseif strcmp(get(hdl_line(i),'UserData'),'y axis')
      line_string{i,1} = ['y axis ',fvar(i,4)]
    elseif i <= len(variabili)
      line_string{i,1} = ['line   ',fvar(i,4),variabili{i}]
    else
      line_string{i,1} = ['symbol ',fvar(i,4), ...
                          variabili{i-len(variabili)}]
  set(hdl_list,'String',line_string,'Value',1)

 case 'axesprops'

  fm_axesdlg(hdlfig)

 case 'textprops'

  TextProp = uisetfont
  if isstruct(TextProp)
    set(hdlfig,TextProp)
    set(get(hdlfig,'XLabel'),TextProp)
    set(get(hdlfig,'YLabel'),TextProp)
    set(get(hdlfig,'Title'),TextProp)
    if get(Hdl_legend,'Value')
      hlegend = findobj(Fig.plot,'Tag','legend')
      hchild = get(hlegend,'Child')
      set(hchild(end), ...
          'FontName',TextProp.FontName, ...
          'FontWeight', TextProp.FontWeight, ...
          'FontAngle',TextProp.FontAngle)

 case 'setxlabel'

  value = get(gcbo,'Value')
  set(gcbo,'Value',value(end))
  if strcmp(get(Fig.plot,'SelectionType'),'open')
    fm_plot('plotvars')

 case 'setangles'

  [idx,kdx] = get_angle_idx
  set(gcbo,'String',[{'None'}; Varname.uvars(idx)],'UserData',kdx)

 case 'limits'

  status = get(gcbo,'Checked')
  switch status
   case 'on'
    set(gcbo,'Checked','off')
   case 'off'
    set(gcbo,'Checked','on')
  fm_plot plotvars

 case 'usedegrees'

  status = get(gcbo,'Checked')
  switch status
   case 'on'
    Settings.usedegree = 0
    set(gcbo,'Checked','off')
   case 'off'
    Settings.usedegree = 1
    set(gcbo,'Checked','on')
  fm_plot plotvars

 case 'usehertzs'

  status = get(gcbo,'Checked')
  switch status
   case 'on'
    Settings.usehertz = 0
    set(gcbo,'Checked','off')
   case 'off'
    Settings.usehertz = 1
    set(gcbo,'Checked','on')
  fm_plot plotvars

 case 'userelspeeds'

  status = get(gcbo,'Checked')
  switch status
   case 'on'
    Settings.userelspeed = 0
    set(gcbo,'Checked','off')
   case 'off'
    Settings.userelspeed = 1
    set(gcbo,'Checked','on')
  fm_plot plotvars

 case 'plotvlims'

  hdl = findobj(Fig.plot,'Tag','PlotVLim')
  value = get(hdl,'Checked')
  if not strcmp(value,'on'), return, end
  xlimits = get(hdlfig,'XLim')
  hold on
  plot(hdlfig,[xlimits(1) xlimits(2)],[0.9 0.9],'k:')
  plot(hdlfig,[xlimits(1) xlimits(2)],[1.1 1.1],'k:')
  hold off

 case 'plotslims'

  hdl = findobj(Fig.plot,'Tag','NormSij')
  value = get(hdl,'Checked')
  if not strcmp(value,'on'), return, end
  xlimits = get(hdlfig,'XLim')
  hold on
  plot(hdlfig,[xlimits(1) xlimits(2)],[1.0 1.0],'k:')
  hold off

 case 'lowestv'

  idx = find(Varname.idx > DAE.n+Bus.n  and  Varname.idx <= DAE.n+2*Bus.n)
  if isempty(idx), return, end
  out = Varout.vars(:,idx)
  vals = min(out,[],1)
  [y,jdx] = sort(vals)
  if len(jdx) > 3, jdx = jdx(1:3); end
  set(Hdl_listvar,'Value',idx(jdx))
  fm_plot listvars
  fm_plot plotvars

 case 'highestv'

  idx = find(Varname.idx > DAE.n+Bus.n  and  Varname.idx <= DAE.n+2*Bus.n)
  if isempty(idx), return, end
  out = Varout.vars(:,idx)
  vals = max(out,[],1)
  [y,jdx] = sort(vals,2,'descend')
  if len(jdx) > 3, jdx = jdx(1:3); end
  set(Hdl_listvar,'Value',idx(jdx))
  fm_plot listvars
  fm_plot plotvars

 case 'highests'

  values = highests(Line)
  if isempty(values), return, end
  set(Hdl_listvar,'Value',values)
  fm_plot listvars
  fm_plot plotvars


if not isempty(Settings.zoom), eval(Settings.zoom), end

# ------------------------------------------------------------------------
# Some useful functions
# -----------------------------------------------------------------------

function stringa = enum(stringa)
for i = 1:len(stringa),
  stringa{i} = ['[',int2str(i),'] ',stringa{i}]

function kdx = get_rotor_idx(idx)
global DAE Syn COI Cswt Dfig Ddsg Busfreq Mass SSR Tg
kdx = []
for i in range(1, len(idx)+1):
  kkk = idx(i)
  if kkk > DAE.n+DAE.m
    break
  elseif kkk <= DAE.n
    if isomega(Syn,kkk)  or  isomega(Cswt,kkk)  or  isomega(Dfig,kkk) ...
         or  isomega(Ddsg,kkk)  or  isomega(Mass,kkk)  or  isomega(SSR,kkk) ...
         or  isomega(Busfreq)
      kdx = [kdx, i]
  elseif isomega(COI,kkk)  or  isomega(Tg,kkk)
    kdx = [kdx, i]

function varargout = get_angle_idx(varargin)
global Varout DAE Syn Bus COI Mass SSR Phs Svc Cswt Ddsg Dfig Pmu Hvdc
idx = []
kdx = []

if not nargin
  varidx = Varout.idx
else
  varidx = varargin{1}

for i in range(1, len(varidx)+1):
  kkk = varidx(i)
  if kkk > DAE.n+DAE.m
    break
  elseif kkk <= DAE.n
    if isdelta(Syn,kkk)  or  isdelta(Mass,kkk)  or  isdelta(SSR,kkk) ...
         or  isdelta(Phs,kkk)  or  isdelta(Svc,kkk)  or  isdelta(Cswt,kkk) ...
         or  isdelta(Ddsg,kkk)  or  isdelta(Dfig,kkk)  or  isdelta(Pmu,kkk)
      idx = [idx, kkk]
      kdx = [kdx, i]
  elseif kkk > DAE.n  and  kkk <= DAE.n+Bus.n
    idx = [idx, kkk]
    kdx = [kdx, i]
  elseif isdelta(COI,kkk)  or  isdelta(Hvdc,kkk)
    idx = [idx, kkk]
    kdx = [kdx, i]

switch nargout
 case 1
  varargout{1} = kdx
 case 2
  varargout{1} = idx
  varargout{2} = kdx