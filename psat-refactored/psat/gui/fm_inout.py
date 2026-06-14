# Module: psat.gui.fm_inout
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_inout():

# FM_INOUT changes inputs & outputs of the current
#          selected Simulink block
#
#see also FM_LIB, FM_SIM, FM_SIMDATA, FM_SIMSETT, FM_BLOCK
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    13-May-2003
#Version:   1.0.1
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings

sys    = get_param(0,'CurrentSystem')
block  = get_param(sys,'CurrentBlock')
gg     = get_param([sys,'/',block],'Selected')
mask   = get_param([sys,'/',block],'MaskType')
object = [sys,'/',block]

Values = get_param(object,'MaskValues')

set_param(object,'LinkStatus','none')

a = get_param(object,'MaskEnables')
b = get_param(object,'MaskPrompts')
buspmc = 0

switch mask
 case 'Bus'
  if len(Values) == 8
    inputs  = floor(str2num(Values{7}))
    outputs = floor(str2num(Values{8}))
    inputs_pmc = floor(str2num(Values{2}))
    outputs_pmc = floor(str2num(Values{1}))
    buspmc = 1
  else
    inputs  = floor(str2num(Values{1}))
    outputs = floor(str2num(Values{2}))
 case 'Wind'
  inputs  = 0
  outputs = floor(str2num(Values{1}))
 case 'Cac'
  inputs  = 1
  outputs = floor(str2num(Values{1}))
 case 'Exc'
  inputs  = floor(str2num(Values{12}))
  outputs = 1
 case 'Syn'
  inputs  = floor(str2num(Values{13}))
  outputs = 1
 case 'Mass'
  inputs  = floor(str2num(Values{5}))
  outputs = 1
 case 'Supply'
  inputs  = floor(str2num(Values{11}))
  outputs = 1
 case 'Demand'
  inputs = 1
  outputs  = floor(str2num(Values{10}))
 case {'Areas','Regions'}
  inputs  = 0
  outputs = floor(str2num(Values{1}))
  buspmc = 1
 otherwise
  fm_choice('Undefined block!',2)
  return

if inputs > Settings.maxsimin  or  outputs > Settings.maxsimout
  if inputs  > Settings.maxsimin
    fm_choice(['Too many inputs. Maximum number is ', ...
               num2str(Settings.maxsimin),'.'],2)
  if outputs > Settings.maxsimout
    fm_choice(['Too many outputs. Maximum number is ', ...
               num2str(Settings.maxsimout),'.'],2)
  return

if not inputs  and  not outputs  and  not buspmc
  fm_choice('Inputs & Outputs cannot be both zero.',2)
  return

BlockType = get_param(object,'BlockType')
if strcmp(BlockType,'PMComponent')
  newl = []
for i in range(1, inputs+1):
    newl = [newl,'|__newl',int2str(i-1)]
  if inputs
    set_param(object,'LConnTagsString',newl(2:end))
  else
    set_param(object,'LConnTagsString','')
  newr = []
for i in range(1, outputs+1):
    newr = [newr,'|__newr',int2str(i-1)]
  if outputs
     set_param(object,'RConnTagsString',newr(2:end))
  else
    set_param(object,'RConnTagsString','')
  return

ori  = get_param(object,'orientation')
posi = get_param(object,'position')
if strcmp(ori,'left')  or  strcmp(ori,'right')
  upperleft=posi(2)
  s=posi(4)-posi(2)
  isop=get_param(object,'InputPorts')
  branches_in=isop(:,2)-upperleft
  isop=get_param(object,'OutputPorts')
  branches_out=isop(:,2)-upperleft
else
  upperleft=posi(3)
  s=posi(3)-posi(1)
  isop=get_param(object,'InputPorts')
  branches_in=isop(:,1)-upperleft
  isop=get_param(object,'OutputPorts')
  branches_out=isop(:,1)-upperleft

if isempty(branches_out)  and  strcmp(mask,'Syn')
  outputs = 0

# Add or remove input and output ports

in=size(branches_in,1)
ou=size(branches_out,1)
if inputs > in,
for i in range(in+1, inputs+1):
    Y1 = (i-1)*50+25
    add_block('built-in/Inport',[object,'/in_',num2str(i)])
    set_param([object,'/in_',num2str(i)],...
              'position',[25,Y1,45,Y1+20],'Port',num2str(i))
    add_block('built-in/Terminator',[object,'/t',num2str(i)])
    set_param([object,'/t',num2str(i)],...
              'position',[80,Y1-5,105,Y1+25])
    add_line(object,['in_',num2str(i),'/1'],['t',num2str(i),'/1'])
if outputs > ou
for i in range(ou+1, outputs+1):
    Y1=(i-1)*50+25
    add_block('built-in/Outport',[object,'/out_',num2str(i)])
    set_param([object,'/out_',num2str(i)],...
              'position',[185,Y1,205,Y1+20],'Port',num2str(i))
    add_block('built-in/constant',[object,'/g',num2str(i)])
    set_param([object,'/g',num2str(i)],...
              'position',[130,Y1-5,155,Y1+25])
    add_line(object,['g',num2str(i),'/1'],['out_',num2str(i),'/1'])
if inputs < in
for i in range(in, inputs+1+1, -1):
    delete_line(object,['in_',num2str(i),'/1'],['t',num2str(i),'/1'])
    delete_block([object,'/in_',num2str(i)])
    delete_block([object,'/t',num2str(i)])
if outputs < ou
for i in range(ou, outputs+1+1, -1):
    delete_line(object,['g',num2str(i),'/1'],['out_',num2str(i),'/1'])
    delete_block([object,'/out_',num2str(i)])
    delete_block([object,'/g',num2str(i)])

if buspmc
   ports = get_param([object,'/pmc'],'Ports')
   ports_in = ports(6)
   ports_out = ports(7)

for i in range(ports_in-1, inputs_pmc+1, -1):
     delete_line(object,['pmc_in_',num2str(i),'/RConn1'],['pmc/LConn',int2str(i+1)])
     delete_block([object,'/pmc_in_',num2str(i)])

for i in range(ports_out-1, outputs_pmc+1, -1):
     delete_line(object,['pmc/RConn',int2str(i+1)],['pmc_out_',int2str(i),'/RConn1'])
     delete_block([object,'/pmc_out_',num2str(i)])

   newl = []
for i in range(1, inputs_pmc+1):
     newl = [newl,'|__newl',int2str(i-1)]
   if inputs_pmc
     set_param([object,'/pmc'],'LConnTagsString',newl(2:end))
   else
     set_param([object,'/pmc'],'LConnTagsString','')
   newr = []
for i in range(1, outputs_pmc+1):
     newr = [newr,'|__newr',int2str(i-1)]
   if outputs_pmc
     set_param([object,'/pmc'],'RConnTagsString',newr(2:end))
   else
     set_param([object,'/pmc'],'RConnTagsString','')

for i in range(ports_in, inputs_pmc-1+1):
     add_block('built-in/PMIOPort',[object,'/pmc_in_',num2str(i)])
     set_param([object,'/pmc_in_',num2str(i)], ...
               'Side','Right', ...
               'Position',[60, 86-15*i, 90, 104-15*i])
     add_line(object,['pmc_in_',num2str(i),'/RConn1'],['pmc/LConn',int2str(i+1)])

for i in range(ports_out, outputs_pmc-1+1):
     add_block('built-in/PMIOPort',[object,'/pmc_out_',num2str(i)])
     set_param([object,'/pmc_out_',num2str(i)], ...
               'Side','Left', ...
               'Orientation','left', ...
               'Position',[260, 86-15*i, 290, 104-15*i])
     add_line(object,['pmc/RConn',int2str(i+1)],['pmc_out_',int2str(i),'/RConn1'])
