# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/pgrep.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def pgrep(expression, string, options):

#PGREP change strings within files
#
#PGREP(EXPRESSION,STRING,TYPE)
#    EXPRESSION: regular expression
#    STRING: the string to be searched.
#    TYPE:   1 - list file names, row number and line text
#            2 - list file names and line text
#            3 - list file names
#            4 - as 1, but look for Matlab variables only
#            5 - as 1, but span all subdirectories
#
#see also PSED
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

if nargin < 3,
  print('Check synthax ...')
  print('   ')
  help pgrep,
  return,
if not ischar(expression)
  print('First argument has to be a not empty string.')
  return
if not ischar(string)  or  isempty(string)
  print('Second argument has to be a not empty string.')
  return
if not isnumeric(options)  or  len(options) > 1  or  rem(options,1)  or  ...
      options > 5  or  options <= 0
  print('Third argument has to be a scalar integer within [1-5]')
  return

a = dir(expression)
if isempty(a)
  print('No file name matches the given expression.')
  return
file = {a.name}';
a = dir(pwd)
names = {a.name}';
isdir = [a.isdir]';
if options == 5,
  print('  ')
  print('Spanning directories ...')
  print('  ')
  print(pwd)
  file = deepdir(expression,names,file,isdir,pwd)
  options = 1
else
  print('  ')
  print(pwd)
n_file = len(file)
if not n_file, print('No matches.'),
  return,
check = 0
try,
  if exist('strfind')
    check = 1
catch
# nothing to do
# this for Octave compatibility

print('  ')
print('Scanning files ...')
print('  ')

for i in range(1, n_file+1):
  fid = fopen(file{i}, 'rt')
  n_row = 0
  while 1  and  fid > 0
    sline = fgets(fid)
    if not isempty(sline),
      if sline == -1,
        break
    n_row = n_row + 1
    if check
      vec = strfind(sline,string)
    else
      vec = findstr(sline,string)
    if not isempty(vec)
      switch options
       case 1
        print([fvar(file{i},14),'  row ',fvar(int2str(n_row),5), ...
              ' >> ',sline(1:end-1)])
       case 3
        print(file{i})
        break
       case 2
        print([fvar(file{i},14),' >> ',sline(1:end-1)])
       case 4
        okdisp = 0
        okdispl = 0
        okdispr = 0
for j in range(1, len(vec)+1):
          if vec(j) > 1,
            ch_l = double(sline(vec(j)-1))
            if ch_l != 34  and  ch_l != 39  and  ch_l != 95  and  ch_l != 46  and  ...
                       (ch_l < 48  or  (ch_l > 57  and  ch_l < 65)  or  ...
                        (ch_l > 90  and  ch_l < 97)  or  ch_l > 122)
              okdispl = 1
          if vec(j) + len(string) < len(sline),
            ch_r = double(sline(vec(j)+len(string)))
            if ch_r != 34  and  ch_r != 95  and  ...
                       (ch_r < 48  or  (ch_r > 57  and  ch_r < 65)  or  ...
                        (ch_r > 90  and  ch_r < 97)  or  ch_r > 122)
              okdispr = 1
          else
            okdispr = 1
          if okdispl  and  okdispr,
            okdisp = 1
            break
          okdispl = 0
          okdispr = 0
        if okdisp,
          print([fvar(file{i},14),'  row ',fvar(int2str(n_row),5), ...
                ' >> ',sline(1:end-1)]),
  if fid > 0,
    count = fclose(fid)

# ----------------------------------------------------------------------
# find subdirectories
# ----------------------------------------------------------------------

function file = deepdir(expression,names,file,isdir,folder)
idx = find(isdir)
for i in range(3, len(idx)+1):
  print([folder,filesep,names{idx(i)}])
  newfolder = [folder,filesep,names{idx(i)}]
  b = dir([newfolder,filesep,expression])
  if not isempty({b.name})
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
