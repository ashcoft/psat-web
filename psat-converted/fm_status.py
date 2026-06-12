# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_status.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_status(varargin):

# FM_STATUS display convergence error of the current simulation in
#           the main window
#
# FM_STATUS('init',xmax,colors,styles,faces)
# FM_STATUS('update',values,iteration,err_max)
#
#see also the structure Hdl
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    09-Jul-2003
#Version:   1.0.1
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings Fig Hdl Theme CPF OPF

persistent handles
persistent status
persistent firstvalue
persistent hdl

if nargin
  routine = varargin{1}
  flag = varargin{2}
else
  return

switch routine
 case 'pf'
  check = Settings.status
 case 'opf'
  check = OPF.show
 case 'cpf'
  check = CPF.show
 case 'lib'
  check = Settings.status
 case 'snb'
  check = Settings.status

if not (Settings.show  and  check  and  ishandle(Fig.main)), return, end

switch flag
 case 'init'

  xmax = varargin{3}
  colors = varargin{4}
  styles = varargin{5}
  faces = varargin{6}
  if nargin > 6
    yrange = varargin{7}
  else
    yrange = [0 1]

  if ishandle(Hdl.status), delete(Hdl.status); end

  hdl = findobj(Fig.main,'Tag','PushClose')
  set(hdl,'String','Stop')
  set(Fig.main,'UserData',1)

  set(0,'CurrentFigure',Fig.main)
  Hdl.status = axes('position',[0.0406 0.1152 0.2537 0.2243])
  if Settings.hostver < 8.04
    set(Hdl.status, ...
        'Drawmode','fast', ...
        'NextPlot','add', ...
        'Color',Theme.color1, ...
        'Xlim',[1 xmax], ...
        'Ylim',yrange, ...
        'Box','on')
  else
    set(Hdl.status, ...
        'NextPlot','add', ...
        'Color',Theme.color04, ...
        'Xlim',[1 xmax], ...
        'Ylim',yrange, ...
        'Box','on')
#'SortMethod','depth', ...
  grid('on')

  handles = np.zeros((len(colors),1))
for i in range(1, len(colors)+1):
    if Settings.hostver < 8.04
      handles(i) = line('Color',colors{i}, ...
                        'LineStyle',styles{i}, ...
                        'Marker','o', ...
                        'MarkerSize',5, ...
                        'XData',[1 1], ...
                        'YData',[100 100], ...
                        'Erase','none', ...
                        'MarkerFaceColor',faces{i})
    else
      handles(i) = line('Color',colors{i}, ...
                        'LineStyle',styles{i}, ...
                        'Marker','o', ...
                        'MarkerSize',5, ...
                        'MarkerFaceColor',faces{i})
  drawnow
  status = []

 case 'update'

  values = varargin{3}
  iteration = varargin{4}

  if iteration == 1
    firstvalue = values(2:end)
    if not firstvalue, firstvalue = 1; end
    values(2:end) = 1
  else
    values(2:end) = abs(values(2:end))./firstvalue

  status = [status; values]

for i in range(1, len(handles)+1):
    if status(1,i+1) == 0
      status(1,i+1) = 1
    if Settings.hostver < 8.04
      set(handles(i), ...
          'xdata',status([max(end-1,1),end],1), ...
          'ydata',status([max(end-1,1),end],i+1))
      drawnow
    else
# display(status(end,1))
# display(status(end,i+1))
# help addpoints
      set(handles(i), ...
          'XData', status([1:end], 1), ...
          'YData', status([1:end], i+1))
      drawnow update

 case 'close'

  set(hdl,'String','Close')

