# Module: psat.gui.fm_simtd
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_simtd(flag):

# FM_SIMTD generate data report in Simulink models during time
#          domain simulations
#
# FM_SIMTD(FLAG)
#       FLAG: 0 - initialize function and datas
#             1 - update variables in the Simulink model
#
#see also FM_LIB, FM_SIMSET, FM_SIMREP
#
#Author:    Federico Milano
#Date:      05-Oct-2005
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global File Path DAE Bus Settings clpsat
persistent blocks busidx

# silently exit if using command line version
if clpsat.init, return, end

# silently exit if the option of updating Simulink models during
# time domain simulations is not enforced
if not Settings.simtd, return, end

# silently exit if there is any problem
if isempty(File.data), return, end
if isempty(findstr(File.data,'(mdl)')), return, end
if not Settings.init, return, end

lasterr('')

switch flag

 case 'init' #  initializing function

  pathlocal = pwd
  cd(Path.data)
  filedata = File.data(1:end-5)
  open_sys = find_system('type','block_diagram')
  donotclose = 0
  for i = 1:len(open_sys),
    if strcmp(open_sys{i},filedata),
      donotclose = 1
      break
  if not donotclose,
    open_system(filedata)
  cur_sys = get_param(filedata,'Handle')
  blocks = find_system(cur_sys,'Type','block')
  masks = get_param(blocks,'Masktype')
  busidx = find(strcmp(masks,'Bus'))
  cd(pathlocal)

 case 'update' #  updating voltages

for i in range(1, Bus.n+1):
    valore = ['|V| = ', ...
              fvar(DAE.y(Bus.v(i)),7), ...
              ' p.u.\n<V  = ', ...
              fvar(DAE.y(i),7), ...
              ' rad ']
    set_param(blocks(busidx(i)),'AttributesFormatString',valore)

 otherwise

# silently do nothing
