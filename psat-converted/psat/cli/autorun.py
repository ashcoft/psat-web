# Module: psat.cli.autorun
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function check = autorun(msg,type)
# AUTORUN properly launch PSAT routine checking for data
#         files and previous power flow solutions
#
# CHECK = AUTORUN(MSG)
#         MSG   message to be displayed
#         TYPE  0 for static analysis, 1 for dynamic analysis
#         CHECK 1 if everything goes fine, 0 otherwise
#
#Author:    Federico Milano
#Date:      29-Oct-2003
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings File Bus
global DAE LIB SNB OPF CPF clpsat Comp

check = 0

# check for data file
if isempty(File.data),
  fm_print(['Set a data file before running ',msg,'.'],2)
  return

# check for initial power flow solution
if not Settings.init
  solvepf
  if not Settings.init, return, end

# check for dynamic components if running a static analysis
if not type  and  DAE.n  and  not clpsat.init
  dynlf = sum(prod(Comp.prop(:,[3 6 9]),2))
  iscpf = strcmp(msg,'Continuation Power Flow')
  if not Settings.static  and  not dynlf
    Settings.ok = 0
    uiwait(fm_choice('Dynamic components will be discarded. Continue?'))
    if Settings.ok
      Settings.static = 1
      solvepf
      Settings.static = 0; #  reset initial condition
    else
      return
  elseif not Settings.static  and  not dynlf  and  iscpf
    Settings.ok = 0
    uiwait(fm_choice(['Dynamic components can lead to numerical ' ...
                      'problems, discard?']))
    if Settings.ok
      Settings.static = 1
      solvepf
      Settings.static = 0; #  reset initial condition
  elseif iscpf
    Settings.ok = 1
#uiwait(fm_choice(['Dynamic components can lead to numerical ' ...
#                  'problems, continue?']))
#if ~Settings.ok, return, end
  else
    uiwait(fm_choice(['Dynamic components are not supported for ' ...
                      'static analysis'],2))
    return

# check for previous CPF & ATC solutions
if strcmp(msg,'SNB Direct Method')
  one = 1
else
  one = 0

if CPF.init  and  not (one  and  CPF.init == 1)
  switch CPF.init
   case 1, met = 'CPF'
   case 2, met = 'ATC'
   case 3, met = 'N-1 Cont. An.'
   case 4, met = 'Continuation OPF (PSAT-GAMS)'
  Settings.ok = 0
  if clpsat.init
    Settings.ok = clpsat.refresh
  else
    uiwait(fm_choice([met,' has been run last. Do you want to' ...
                      ' restore initial PF solution?']))
  if Settings.ok
    solvepf
    fm_print(['Initial PF solution will be used as ', ...
	     'base case solution.'])
  else
    fm_print(['Last ',met,' solution will be used as ', ...
	     'base case solution.'])
  CPF.init = 0

# check for previous time domain simulations
if Settings.init == 2
  Settings.ok = 0
  if clpsat.init
    Settings.ok = clpsat.refresh
  else
    uiwait(fm_choice(['TD has been run last. Do you want to' ...
                      ' restore initial PF solution?']))
  if Settings.ok
    solvepf
    fm_print(['Initial PF solution will be used as ', ...
	     'base case solution.'])
  else
    fm_print('Last TD point will be used as base case solution.')
  Settings.init = 1

# check for SNB direct method
if SNB.init
  Settings.ok = 0
  if clpsat.init
    Settings.ok = clpsat.refresh
  else
    uiwait(fm_choice(['SNB direct method has been run last. Do you want to' ...
                      ' restore initial PF solution?']))
  if Settings.ok
    solvepf
    fm_print(['Initial PF solution will be used as ', ...
	     'base case solution.'])
  else
    fm_print('SNB solution will be used as base case solution.')
  SNB.init = 0

# check for LIB direct method
if LIB.init
  Settings.ok = 0
  if clpsat.init
    Settings.ok = clpsat.refresh
  else
    uiwait(fm_choice(['LIB direct method has been run last. Do you want to' ...
                      ' restore initial PF solution?']))
  if Settings.ok
    solvepf
    fm_print('Initial PF solution will be used as base case solution.')
  else
    fm_print('LIB solution will be used as base case solution.')
  LIB.init = 0

# check for OPF solution
if strcmp(msg,'Optimal Power Flow')
  one = 0
else
  one = 1

if OPF.init  and  one
  Settings.ok = 0
  if clpsat.init
    Settings.ok = clpsat.refresh
  else
    uiwait(fm_choice(['OPF has been run last. Do you want to' ...
                      ' restore initial PF solution?']))
  if Settings.ok
    solvepf
    fm_print(['Initial PF solution will be used as ', ...
	     'base case solution.'])
  else
    fm_print('OPF solution will be used as base case solution.')
  OPF.init = 0

check = 1

# ---------------------------------------------------
def solvepf():

global Settings Varname

fm_print('Solve base case power flow...')
varname_old = Varname.idx
Settings.show = 0
fm_set('lf')
Settings.show = 1
if not isempty(varname_old)
  Varname.idx = varname_old