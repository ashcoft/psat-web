# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_writetxt.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_writetxt(Matrix, Header, Cols, Rows, File):

# FM_WRITETXT export PSAT results to a plain ASCII file.
#
# FM_WRITETXT(MATRIX,HEDAER,COLNAMES,ROWNAMES,FILENAME)
#
#    MATRIX     Matrix to write to file
#               Cell array for multiple matrices.
#    HEADER     String of header information.
#               Cell array for multiple header.
#    COLNAMES   (Cell array of strings) Column headers.
#               One cell element per column.
#    ROWNAMES   (Cell array of strings) Row headers.
#               One cell element per row.
#    FILENAME   (string) Name of text file.
#               If not specified, contents will be
#               opened in the current selected text
#               viewer.
#
#Author:    Federico Milano
#Date:      14-Sep-2003
#Version:   1.0.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Path

if not iscell(Matrix)
  Matrix{1,1} = Matrix
  Header{1,1} = Header
  Cols{1,1} = Cols
  Rows{1,1} = Rows

if strcmp(Header{1,1}{1,1},'EIGENVALUE REPORT')
  Eigs = 1
  num = 18
else
  Eigs = 0
  num = 12

# --------------------------------------------------------------------
# opening text file
# --------------------------------------------------------------------

fm_disp
fm_print('Opening the report file...')

[fid,msg] = fopen([Path.data,File], 'wt')
if fid == -1
  fm_print(msg)
  return

# --------------------------------------------------------------------
# writing data
# --------------------------------------------------------------------

nhr = 0

for i_matrix in range(1, len(Matrix)+1):

  m = Matrix{i_matrix}
  colnames = Cols{i_matrix}
  rownames = Rows{i_matrix}
  header = Header{i_matrix}

# Write header
# ------------------------------------------------------------------

  if not isempty(header)
    if iscell(header)
for ii in range(1, len(header)+1):
        count = fprintf(fid,'%s\n',header{ii})
    elseif not isempty(header)
      count = fprintf(fid,'%s\n',header)
    count = fprintf(fid,'\n')

# Write column names
# ------------------------------------------------------------------

  if nargin > 2  and  not isempty(colnames)
    [nrows,ncolnames] = size(colnames)
for jj in range(1, nrows+1):
for ii in range(1, ncolnames+1):
        if Eigs  and  i_matrix == 2  and  ii == 2
#  and  length({rownames{ii,:}}) == 2
          num = 28
        elseif Eigs
          num = 15
        else
          num = 12
        count = fprintf(fid, '%s', fvar(colnames{jj,ii},num))
      count = fprintf(fid,'\n')
    count = fprintf(fid,'\n')

# Write data
# ------------------------------------------------------------------

  if nargin > 3  and  not isempty(rownames)
    [nrownames,ncols] = size(rownames)
    ndata = size(m,2)
for ii in range(1, nrownames+1):
for jj in range(1, ncols+1):
        if Eigs  and  i_matrix == 2  and  jj == 2
          num = 28
        elseif Eigs
          num = 15
        else
          num = 12
        if isempty(colnames)
          nchar = 30
        else
          nchar = num
        if jj == ncols, nchar = nchar - 1; end
        count = fprintf(fid, '%s ', fvar(rownames{ii,jj},nchar-1))
for hh in range(1, ndata+1):
        if Eigs
          num = 15
        else
          num = 12
	count = fprintf(fid, '%s', fvar(m(ii,hh),num))
      count = fprintf(fid,'\n')
  count = fprintf(fid,'\n')


fclose(fid)
fm_print(['Report of Static Results saved in text file "',Path.data,File,'" '])

# view file
fm_text(13,[Path.data,File])