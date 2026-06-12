# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_writetex.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fm_writetex(Matrix, Header, Cols, Rows, File):

# FM_WRITETEX export PSAT results in LaTeX2e format.
#
# FM_WRITETEX(MATRIX,HEDAER,COLNAMES,ROWNAMES,FILENAME)
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
#Date:      15-Sep-2003
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
fm_print('Writing the report LaTeX2e file...')

[fid,msg] = fopen([Path.data,File], 'wt')
if fid == -1
  fm_print(msg)
  return
path_lf = strrep(Path.data,'\','\\')

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

# treat header as comment
    if not isempty(header)
      if iscell(header)
for ii in range(1, len(header)+1):
          count = fprintf(fid,'%% %s\n',specialchar(header{ii}))
      else
        count = fprintf(fid,'%% %s\n',specialchar(header))

  else #  create table

    idx_table = idx_table + 1

# print the preamble of the table
# see Leslie Lamport's LATEX book for details.
# open the table environment as a floating body
    fprintf(fid, '\\begin{table}[htbp] \n')
    fprintf(fid, ' \\begin{center} \n')

# Write header
# ------------------------------------------------------------------

    caption = ''
    if iscell(header)
for ii in range(1, len(header)+1):
	caption = [caption,' ',header{ii}]
    else
      caption = [caption,header]
    caption = specialchar(caption)

#% include the user-defined or default caption
    fprintf(fid, '  \\caption{%s} \n', caption)
    count = fprintf(fid,'  \\vspace{0.1cm}\n')

# Write column names
# ------------------------------------------------------------------

    if nargin > 2  and  not isempty(colnames)
      [nrows,ncolnames] = size(colnames)

      tt =  '|'
for ii in range(1, ncolnames+1):
	tt = [tt,'c|']
      fprintf(fid, '  \\begin{tabular}{%s} \n', tt)
      fprintf(fid, '   \\hline \n')

for jj in range(1, nrows+1):
	fprintf(fid, '   ')
for ii in range(1, ncolnames-1+1):
	  count = fprintf(fid, '%s & ', specialchar(colnames{jj,ii}))
	count = fprintf(fid, '%s \\\\\n', specialchar(colnames{jj,ncolnames}))
      count = fprintf(fid,'   \\hline \\hline \n')

# Write data
# ------------------------------------------------------------------

    if nargin > 3  and  not isempty(rownames)
      [nrownames,ncols] = size(rownames)
      ndata = size(m,2)

      if isempty(colnames)
	tt =  '|'
for ii in range(1, (ncols+ndata)+1):
	  tt = [tt,'c|']
	fprintf(fid, '  \\begin{tabular}{%s} \n', tt)
	fprintf(fid, '   \\hline \n')

for ii in range(1, nrownames+1):
	fprintf(fid, '   ')
for jj in range(1, ncols+1):
	  count = fprintf(fid, '%s & ', specialchar(rownames{ii,jj}))
for hh in range(1, ndata-1+1):
	  count = fprintf(fid, '$%8.5f$ & ', m(ii,hh))
	count = fprintf(fid, '$%8.5f$ \\\\ \\hline \n', m(ii,ndata))

#% print the footer of the table environment
    fprintf(fid, '  \\end{tabular} \n')
#% include the user-defined or default label
    fprintf(fid, '  \\label{%s} \n', ...
	    ['tab:',strrep(File,'.tex',''),'_',num2str(idx_table)])
    fprintf(fid, ' \\end{center} \n')
#% close the table environment and return
    fprintf(fid, '\\end{table} \n')

  count = fprintf(fid,'\n')


fclose(fid)
fm_print(['Report of Static Results saved in ',File])

# view file
fm_text(13,[Path.data,File])


# -------------------------------------------------------
# check for special LaTeX2e character
# -------------------------------------------------------

function string = specialchar(string)

string = [lower(strrep(string,'#','\#')),' ']
string = strrep(string,'&','\&')
string = strrep(string,'_','\_')
string = strrep(string,'$','\$')
string = strrep(string,'{','\{')
string = strrep(string,'}','\}')
string = strrep(string,'%','\%')
string = strrep(string,'~','$\sim$')
string(1) = upper(string(1))