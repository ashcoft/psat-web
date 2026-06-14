# Module: psat.core.psed
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def psed(expression, string1, string2, type):

#PSED change strings within files
#
#PSED(EXPRESSION,STRING1,STRING2,TYPE)
#    EXPRESSION: regular expression
#    STRING1: the string to be changed.
#    STRING2: the new string
#    TYPE:    1 - change all the occurrence
#             2 - change only Matlab variable type
#             3 - as 2 but no file modifications
#             4 - as 1 but span all subdirectories
#
#see also PGREP
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    18-Feb-2003
#Update:    30-Mar-2004
#Version:   1.0.2
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

if nargin < 4,
  print('Check synthax ...')
  print('  ')
  help psed,
  return,
if not ischar(expression)
  print('First argument (EXPRESSION) has to be a string.')
  return
if not ischar(string1)  or  isempty(string1),
  print('Second argument (STRING1) has to be a string.')
  return
if not ischar(string2)
  print('Third argument (STRING2) has to be a string.')
  return
if isempty(string2)
  string2 = ''
if not isnumeric(type)  or  len(type) > 1  or  rem(type,1)  or  type > 4  or  ...
      type <= 0
  print('Fourth argument has to be a scalar integer [1-4]')
  return

a = dir(expression)
if isempty(a)
  print('No file name matches the given expression.')
  return
file = {a.name}';
a = dir(pwd)
names = {a.name}';
isdir = [a.isdir]';
if type == 4,
  print(' ')
  print('Spanning directories ...')
  print('  ')
  print(pwd)
  file = deepdir(expression,names,file,isdir,pwd)
  type = 1
else
  print('   ')
  print(pwd)

n_file = len(file)
if not n_file, print('No matches.'),
  return,

tipo = type
if tipo == 3,
  tipo = 2
trova = 0
try,
  if exist('strfind')
    trova = 1
catch
# nothing to do
# this is for Octave compatibility

print('   ')
print('Scanning files ...')
print('  ')

for i in range(1, n_file+1):

  fid = fopen(file{i}, 'rt')
  n_row = 0
  match = 0

  while 1  and  fid > 0

    sline = fgetl(fid)
    if not isempty(sline),
      if sline == -1,
        break
    n_row = n_row + 1
    if trova
      vec = strfind(sline,string1)
    else
      vec = findstr(sline,string1)
    slinenew = sline

    if not isempty(vec)

      switch tipo
       case 1

        match = 1
        slinenew = strrep(sline,string1,string2)
        print([fvar(file{i},14),'  row ',fvar(int2str(n_row),5), ...
              ' >> ',slinenew(1:end)])
        print(['                             ',sline])

       case 2

        ok = 0
        okdisp = 0
        okdispl = 0
        okdispr = 0
        count = 0
for j in range(1, len(vec)+1):
          if vec(j) > 1,
            ch_l = double(sline(vec(j)-1))
            if ch_l != 34  and  ch_l != 39  and  ch_l != 95  and  ...
                       ch_l != 46  and  (ch_l < 48  or  (ch_l > 57  and  ch_l < 65)  or  ...
                                     (ch_l > 90  and  ch_l < 97)  or  ch_l > 122)
              okdispl = 1
          else
            okdispl = 1
          if vec(j) + len(string1) < len(sline),
            ch_r = double(sline(vec(j)+len(string1)))
            if ch_r != 34  and  ch_r != 95  and  ...
                       (ch_r < 48  or  (ch_r > 57  and  ch_r < 65)  or  ...
                        (ch_r > 90  and  ch_r < 97)  or  ch_r > 122)
              okdispr = 1
          else
            okdispr = 1
          if okdispl  and  okdispr, okdisp = 1; end
          okdispl = 0
          okdispr = 0
          if okdisp
            count = count + 1
            iniz = vec(j)-1+(count-1)*(len(string2)-len(string1))
            slinenew = [slinenew(1:iniz),string2, ...
                        sline(vec(j)+len(string1):end)]
            ok = 1
          okdisp = 0
        if ok,
          print([fvar(file{i},14),'  row ',fvar(int2str(n_row),5), ...
                ' >> ',slinenew(1:end)])
          print(['                         ',sline])
          match = 1
    newfile{n_row,1} = slinenew
  if fid > 0,
    count = fclose(fid)

  if match  and  type != 3
    fid = fopen(file{i}, 'wt')
    if fid > 0
      for i = 1:n_row-1,
        count = fprintf(fid,'%s\n',deblank(newfile{i}))
      count = fprintf(fid,'%s',deblank(newfile{n_row}))
      count = fclose(fid)

# ---------------------------------------------------------------------
# find subdirectories
# ---------------------------------------------------------------------
function file = deepdir(expression,names,file,isdir,folder)
idx = find(isdir)
for i in range(3, len(idx)+1):
  print([folder,filesep,names{idx(i)}])
  newfolder = [folder,filesep,names{idx(i)}]
  b = dir([newfolder,filesep,expression])
  if not isempty({b.name}),
    bnames = {b.name}
    n = len(bnames)
    newfiles = cell(n,1)
for k in range(1, n+1):
      newfiles{k} = [folder,filesep,names{idx(i)},filesep,bnames{k}]
    file = [file; newfiles]
  b = dir([newfolder])
  newdir = [b.isdir]';
  newnames = {b.name}';
  file = deepdir(expression,newnames,file,newdir,newfolder)