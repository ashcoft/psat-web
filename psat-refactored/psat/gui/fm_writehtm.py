# Module: psat.gui.fm_writehtm
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_writehtm(Matrix, Header, Cols, Rows, File):

# FM_WRITEHTM export PSAT results in HTML format.
#
# FM_WRITEHTM(MATRIX,HEDAER,COLNAMES,ROWNAMES,FILENAME)
#
#    MATRIX     Matrix to write to file
#               Cell array for multiple matrices.
#    HEADER     String of header information.
#               Cell array for multiple header.
#    COLNAMES   (Cell array of strings) Column headers.
#               One cell element per column.
#    ROWNAMES   (Cell array of strings) Row headers.
#               One cell element per row.
#    FILENAME   (string) Name of TeX file.
#               If not specified, contents will be
#               opened in the current selected text
#               viewer.
#
#Author:    Federico Milano
#Date:      28-Apr-2006
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

# --------------------------------------------------------------------
# opening text file
# --------------------------------------------------------------------

fm_disp
fm_print('Writing the report HTML file...')

[fid,msg] = fopen([Path.data,File], 'wt')
if fid == -1
  fm_print(msg)
  return
path_lf = strrep(Path.data,'\','\\')

# --------------------------------------------------------------------
# writing headers and general settings
# --------------------------------------------------------------------

fprintf(fid,'%s\n',['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" ' ...
                    '"http://www.w3.org/TR/html4/strict.dtd">'])
fprintf(fid,'%s\n','<html>')
fprintf(fid,'%s\n','<head>')
fprintf(fid,'%s\n','<title>template.html</title>')
fprintf(fid,'%s\n','<meta name="generator" content="PSAT 2">')
fprintf(fid,'%s\n','<meta name="author" content="Federico Milano">')
fprintf(fid,'%s\n',['<meta name="date" content="',date,'">'])
fprintf(fid,'%s\n','<meta name="copyright" content="Federico Milano">')
fprintf(fid,'%s\n','<meta name="keywords" content="">')
fprintf(fid,'%s\n','<meta name="description" content="">')
fprintf(fid,'%s\n','<meta name="ROBOTS" content="NOINDEX, NOFOLLOW">')
fprintf(fid,'%s\n','<meta http-equiv="content-type" content="text/html; charset=UTF-8">')
fprintf(fid,'%s\n','<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8">')
fprintf(fid,'%s\n','<meta http-equiv="content-style-type" content="text/css">')
fprintf(fid,'%s\n','<meta http-equiv="expires" content="0">')
fprintf(fid,'%s\n','</head>')
fprintf(fid,'%s\n','<body>')

# --------------------------------------------------------------------
# writing data
# --------------------------------------------------------------------

nhr = 0
idx_table = 0

for i_matrix in range(1, len(Matrix)+1):

  m = Matrix{i_matrix}
  colnames = Cols{i_matrix}
  rownames = Rows{i_matrix}
  header = Header{i_matrix}

  if isempty(colnames)  and  isempty(rownames)  and  isempty(m)

    count = fprintf(fid,'%s\n','<div>')
    count = fprintf(fid,'%s\n','<table>')

    if not isempty(header)
      if iscell(header)
	count = fprintf(fid,'%s\n',['<h3> ',header{1},' </h3>'])
for ii in range(2, len(header)+1):
          count = fprintf(fid,'%s\n',['<tr><td> ',header{ii},' </td></tr>'])
      else
        count = fprintf(fid,'%s\n',['<h4> ',header,' </h4>'])
      count = fprintf(fid,'%s\n','</table>')

  else #  create table

    idx_table = idx_table + 1

# Write header
# ------------------------------------------------------------------

    count = fprintf(fid,'%s\n','<div>')
    if iscell(header)
for ii in range(1, len(header)+1):
	count = fprintf(fid,'%s\n',['<h4> ',header{ii},' </h4>'])
    else
      count = fprintf(fid,'%s\n',['<h4> ',header,' </h4>'])
    count = fprintf(fid,'%s\n','<table border="1" rules="all">')

# Write column names
# ------------------------------------------------------------------

    if nargin > 2  and  not isempty(colnames)
      [nrows,ncolnames] = size(colnames)

for jj in range(1, nrows+1):
        count = fprintf(fid,'%s\n','<tr>')
for ii in range(1, ncolnames+1):
	  count = fprintf(fid,'%s\n',['<td> ',colnames{jj,ii},' </td>'])
        count = fprintf(fid,'%s\n','</tr>')

# Write data
# ------------------------------------------------------------------

    if nargin > 3  and  not isempty(rownames)
      [nrownames,ncols] = size(rownames)
      ndata = size(m,2)

for ii in range(1, nrownames+1):
	fprintf(fid, '   ')
        count = fprintf(fid,'%s\n','<tr>')
for jj in range(1, ncols+1):
	  count = fprintf(fid,'%s\n',['<td> ',rownames{ii,jj},' </td>'])
for hh in range(1, ndata+1):
	  count = fprintf(fid,'%s %8.5f %s\n','<td>',m(ii,hh),'</td>')
        count = fprintf(fid,'%s\n','</tr>')
    count = fprintf(fid,'%s\n','</table>')
    count = fprintf(fid,'%s\n','</div>')



# --------------------------------------------------------------------
# writing end of file
# --------------------------------------------------------------------

fprintf(fid,'%s\n','</body>')
fprintf(fid,'%s\n','</html>')

fclose(fid)
fm_print(['Report of Static Results saved in ',File])

# view file
fm_text(13,[Path.data,File])