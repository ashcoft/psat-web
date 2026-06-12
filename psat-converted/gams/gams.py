# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/gams\gams.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function varargout = gams(varargin)
# GAMS general Matlab-GAMS interface function
#
# (...) = GAMS(...)
#
#Author:    Federico Milano
#Date:      01-Mar-2003
#Version:   1.0.0
#
#E-mail:    fmilano@thunderbox.uwaterloo.ca
#Web-site:  http://thunderbox.uwaterloo.ca/~fmilano

gams_output = 'struct'
gams_show = 'minimized'
gams_write_data = 'yes'

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# General settings
#-----------------------------------------------------------------
#-----------------------------------------------------------------

warning off
try, 
  gams_output = evalin('caller','gams_output')
  gams_output = lower(gams_output)
try, 
  gams_show = evalin('caller','gams_show')
  gams_show = lower(gams_show)
try, 
  gams_write_data = evalin('caller','gams_write_data')
  gams_write_data = lower(gams_write_data)
warning on

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Reading input data files:   matglobs.gms
#                             matdata.gms
#-----------------------------------------------------------------
#-----------------------------------------------------------------

if not strcmp(gams_write_data,'no')
  
  fid1 = 0
  fid2 = 0
  
  if not nargin
    print('Specify an input file')
    return
  
  if nargin > 1
    fid1 = fopen('matglobs.gms','wt+')
    fid2 = fopen('matdata.gms','wt+')
  
  if fid2, 
    fprintf(fid2,'%s\n','$onempty')
  
for i in range(2, nargin+1):
    
    if isstr(varargin{i})
      
      fprintf(fid1,'$setglobal %s ''%s''\n',inputname(i), ...
              varargin{i})

    elseif isnumeric(varargin{i})
      
      fprintf(fid2,'$kill %s\n',inputname(i))
      if islogical(varargin{i})
        fprintf(fid2,'set %s /',inputname(i))
      elseif len(varargin{i}) == 1
        fprintf(fid2,'scalar %s /',inputname(i))
      else
        fprintf(fid2,'parameter %s /',inputname(i))
      
      if len(varargin{i}) == 1
        fprintf(fid2,'%f/;\n',varargin{i})
      else    
        fprintf(fid2,'\n')
        h = find(varargin{i})
        siz = size(varargin{i})
        if not isempty(find(siz == 1))
          n = 1
        else
          n = len(siz)
        k = [1 cumprod(siz(1:end-1))]
for j in range(1, len(h)+1):
          string = ['     ',sprintf('%f',varargin{i}(h(j)))]
# ------------------------------------
# ind2sub
          ndx = h(j) - 1
          for ii = n:-1:1,
            idx = floor(ndx/k(ii))+1
            string = ['.',num2str(idx),string]
            ndx = rem(ndx,k(ii))
# ------------------------------------
          fprintf(fid2,'%s\n',string(2:end))
        fprintf(fid2,'/;\n')

    elseif isstruct(varargin{i})
      
      if isstr(varargin{i}.val)
        fprintf(fid1,'$setglobal %s ''%s''\n',varargin{i}.name, ...
                varargin{i}.val)
        continue
            
      if not isfield(varargin{i},'labels')
        siz = size(varargin{i}.val)
        if len(siz) == 2  and  min(siz) == 1
          labels = cellstr(num2str([1:max(siz)]'));
        else
          labels = cell(1,len(siz))
for ii in range(1, len(siz)+1):
            labels{ii} = cellstr(num2str([1:siz(ii)]'));
      else
        labels = varargin{i}.labels
      
      fprintf(fid2,'$kill %s\n',varargin{i}.name)
      if islogical(varargin{i}.val)
        fprintf(fid2,'set %s /\n',varargin{i}.name)
      else
        fprintf(fid2,'parameter %s /\n',varargin{i}.name)
      if not iscell(labels{1})        
        h = find(varargin{i}.val)
        if islogical(varargin{i}.val)
for j in range(1, len(h)+1):
            fprintf(fid2,'%s \n',labels{h(j)})
        else
for j in range(1, len(h)+1):
            fprintf(fid2,'%s %f\n',labels{h(j)}, ...
                    varargin{i}.val(h(j)))
      else        
        h = find(varargin{i}.val)
        siz = size(varargin{i}.val)
        n = len(siz)
        k = [1 cumprod(siz(1:end-1))]
for j in range(1, len(h)+1):
          string = ['     ',sprintf('%f',varargin{i}.val(h(j)))]
# ------------------------------------
# ind2sub
          ndx = h(j) - 1
          for ii = n:-1:1,
            idx = floor(ndx/k(ii))+1
            string = ['.',labels{ii}{idx},string]
            ndx = rem(ndx,k(ii))
# ------------------------------------          
          fprintf(fid2,'%s\n',string(2:end))
      fprintf(fid2,'/;\n')


  
  if fid2, 
    fprintf(fid2,'%s\n','$offempty')
  
  if nargin > 1
    fclose(fid1)
    fclose(fid2)


#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Calling GAMS
#-----------------------------------------------------------------
#-----------------------------------------------------------------

if ispc  and  strcmp(gams_show,'normal')
  eval(['!gams ',varargin{1},' &'])
else
  eval(['!gams ',varargin{1}])

#-----------------------------------------------------------------
#-----------------------------------------------------------------
# Writing output file:    matsol.gms
#-----------------------------------------------------------------
#-----------------------------------------------------------------

if nargout, 
  fid = fopen('matsol.gms','rt+')
  n_out = 0
  d_out = 0
  s_out = []
  t_out = ''
  while 1

    if n_out > nargout, break, end
    tline = fgetl(fid)
    if not ischar(tline), break, end    
    tline = deblank(tline)
    
# ----------------------------------------------------------------
    if isempty(tline)
# ----------------------------------------------------------------
      
# no actions
    
# ----------------------------------------------------------------
    elseif strmatch('::',tline), #  new output variable
# ----------------------------------------------------------------
    
      n_out = n_out+1
      if not strcmp(gams_output,'std')
        varargout{n_out}.name = strrep(tline,'::','')
      
# ----------------------------------------------------------------
    elseif strmatch('d',tline), #  numeric data output
# ----------------------------------------------------------------
      
      s_out = str2num(strrep(tline,'d',''))
      d_out = s_out(1)
      s_out = s_out(2:end)
      t_out = 'nums'

      if strcmp(gams_output,'std')      
        if d_out == 1
          varargout{n_out} = np.zeros((s_out,1))
        else
          varargout{n_out} = np.zeros((s_out))
      else
        if d_out == 1
          varargout{n_out}.val = np.zeros((s_out,1))
        else
          varargout{n_out}.val = np.zeros((s_out))
      
# ----------------------------------------------------------------
    elseif strmatch('c',tline), #  cell array data output
# ----------------------------------------------------------------
    
      s_out = str2num(strrep(tline,'c',''))
      d_out = s_out(1)
      s_out = s_out(2:end)
      t_out = 'cell'
      if strcmp(gams_output,'std')  
        if d_out == 1        
          varargout{n_out} = cell(s_out,1)
        else
          varargout{n_out} = cell(s_out)
      else
        if d_out == 1        
          varargout{n_out}.val = cell(s_out,1)
        else
          varargout{n_out}.val = cell(s_out)
    
# ----------------------------------------------------------------
    else #  fill up elements
# ----------------------------------------------------------------
      
      tline = lower(strrep(tline,'EPS',num2str(eps)))
      switch t_out
       case 'cell'
              
        data = sscanf(tline,['%d',repmat('.%d',1,d_out-1),' %s'])
        if max(s_out) == 1  and  d_out == 1 
          if strcmp(gams_output,'std')  
            varargout{n_out} = char(data(2:end))';                 
          else            
            varargout{n_out}.val = char(data(2:end))';
        else          
# sub2ind
# --------------------------------
          k = [1 cumprod(s_out(1:end-1))]
          ndx = 1
          for i = 1:d_out,
            ndx = ndx + (data(i)-1)*k(i)
# --------------------------------          
          if strcmp(gams_output,'std')  
            varargout{n_out}{ndx} = char(data(d_out+1:end))';                 
          else            
            varargout{n_out}.val{ndx} = char(data(d_out+1:end))';
          
       case 'nums'
        
        data = sscanf(tline,['%d',repmat('.%d',1,d_out-1),' %f'])
# sub2ind
# --------------------------------
        k = [1 cumprod(s_out(1:end-1))]
        ndx = 1
        for i = 1:d_out,
          ndx = ndx + (data(i)-1)*k(i)
# --------------------------------        
        if strcmp(gams_output,'std')  
          varargout{n_out}(ndx) = data(d_out+1)
        else
          varargout{n_out}.val(ndx) = data(d_out+1)
        
      
# ----------------------------------------------------------------
      
  
  fclose(fid)
  if n_out < nargout
for i in range(n_out+1, nargout+1):
      varargout{i}.val = []
  

