# Module: psat.gui.fm_save
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_save(Comp):

# FM_SAVE save UDM to file
#
# FM_SAVE uses the component name COMP.NAME as file name
# and creates a Matlab script.
# The file is saved in the folder ./psat/build
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    15-Sep-2003
#Version:   2.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Settings Path Fig
global Algeb Buses Initl Param Servc State

# check for component name
if isempty(Comp.name)
  fm_print('No component name set.',2)
  return

# check for older versions
a = dir([Path.build,'*.m'])
b = {a.name}
older = strmatch([Comp.name,'.m'],b,'exact')
if not isempty(older)
  uiwait(fm_choice(['Overwrite Existing File "',Comp.name,'.m" ?']))
  if not Settings.ok, return, end

# save data
if isempty(Comp.init)
  Comp.init = 0
if isempty(Comp.descr)
  Comp.descr = ['DAE function ', Comp.name, '.m']

[fid,msg] = fopen([Path.build,Comp.name,'.m'],'wt')
if fid == -1
  fm_print(msg,2)
  fm_print(['UDM File ',Comp.name,'.m couldn''t be saved.'],2)
  return

count = fprintf(fid,'%% User Defined Component %s\n',Comp.name)
count = fprintf(fid,'%% Created with PSAT v%s\n',Settings.version)
count = fprintf(fid,'%% \n')
count = fprintf(fid,'%% Date: %s\n',datestr(now,0))

Comp = rmfield(Comp,{'names','prop','n'})

savestruct(fid,Comp)
savestruct(fid,Buses)
savestruct(fid,Algeb)
savestruct(fid,State)
savestruct(fid,Servc)
savestruct(fid,Param)
savestruct(fid,Initl)

count = fprintf(fid,'\n')
fclose(fid)

fm_print(['UDM File ',Comp.name,'.m saved in folder ./build'])

# update list in the component browser GUI
if ishandle(Fig.comp)
  fm_comp clist

# -------------------------------------------------------------------
function savestruct(fid,structdata)

if isempty(structdata)
  return

if not isstruct(structdata)
  return

fields = fieldnames(structdata)
namestruct = inputname(2)
count = fprintf(fid,'\n%% Struct: %s\n',namestruct)

for i in range(1, len(fields)+1):

  field = getfield(structdata,fields{i})

  if isempty(field)
    count = fprintf(fid,'\n%s.%s = [];',namestruct,fields{i})
  [m,n] = size(field)

  if isnumeric(field)
for mi in range(1, m+1):
for ni in range(1, n+1):
	count = fprintf(fid,['\n%s.%s(%d,%d) = %d;'], ...
			namestruct,fields{i},mi,ni,field(mi,ni))
  elseif iscell(field)
for mi in range(1, m+1):
for ni in range(1, n+1):
	count = fprintf(fid,['\n%s.%s{%d,%d} = ''%s'';'], ...
			namestruct,fields{i},mi,ni, ...
                        strrep(field{mi,ni},'''',''''''))
  elseif ischar(field)
    count = fprintf(fid,'\n%s.%s = ''%s'';', ...
                    namestruct,fields{i},strrep(field,'''',''''''))
  count = fprintf(fid,'\n')
