# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/fm_nrlf.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function    conv = fm_nrlf(varargin)
# FM_NRLF solve power flow with locked ste variables
#
# CONV = FM_NRLF(ITERMAX,TOL,SHOW,INITV)
#       ITERMAX = max number of iterations
#       TOL = convergence tolerance
#       SHOW = 1 to show convergence result, 0 otherwise
#       INITV = 1 to initialize voltages, 0 otherwise
#       CONV = 1 if convergence reached, 0 otherwise
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    11-Sep-2003
#Version:   1.1.0
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global DAE Bus Line PV SW Syn Settings

conv = 1
angles = DAE.y(Bus.a)

switch nargin
 case 0
  iter_max = Settings.lfmit
  tol = Settings.lftol
  Show = 0
  initV = 0
 case 3
  iter_max = varargin{1}
  tol = varargin{2}
  Show = varargin{3}
  initV = 0
 case 4
  iter_max = varargin{1}
  tol = varargin{2}
  Show = varargin{3}
  initV = varargin{4}

check = 1

while check

# initialize bus voltages
  if initV
    DAE.y(Bus.v) = 1.05*getnp.ones((Bus))
    DAE.y(getbus(PV,'v')) = getvg(PV,'all')
    DAE.y(getbus(SW,'v')) = getvg(SW,'all')

# initialize bus angles
    if Syn.n  and  not SW.n

      if check == 1
# try bus angles of last iteration.
# In most cases this is good enough.
        fm_print('Trying last solution bus angle values')
        check = check + 1

      if check == 2
# try an average angle value based on generator rotor
# angles.  Sometimes it works...
        fm_print('Trying average bus angle values')
        DAE.y(Bus.a) = mean(getdelta(Syn))*getnp.ones((Bus))
        DAE.y(getbus(Syn)) = approxdelta(Syn)
#check = check + 1;
        check = 0

      if check > 2
# try a more sophisticated bus angle guess.
# Not sure it works.  Last attempt before giving up...
        fm_print('Trying weighted bus angle values')
        [gen,ib] = setdiff(getbus(Syn),Bus.island)
        loads = setdiff(Bus.a,gen)
        delta = approxdelta(Syn)
        theta = -[imag(Line.Y(loads,loads))]\[imag(Line.Y(loads,gen))*delta(ib)]
        DAE.y(getbus(Syn)) = delta
        DAE.y(loads) = theta
        check = 0

    else
# if there is a slack bus, use it as reference.
      DAE.y(Bus.a) = DAE.y(SW.refbus(1))*getnp.ones((Bus))
      check = 0

  iteration = 0
  inc = np.ones((DAE.m,1))

# Newton-Raphson routine with locked state variables
  while max(abs(inc)) > tol  and  iteration < iter_max

    fm_call('n')  #  call algebraic functions
    fm_setgy(SW.refbus)
    DAE.g(SW.refbus) = 0

    inc = -DAE.Gy\DAE.g
    DAE.y = DAE.y + inc
    iteration = iteration + 1

  if min(DAE.y(Bus.v)) > 0  and  iteration < iter_max
    check = 0


DAE.y(find(DAE.y(Bus.v) <= 1e-6)) = 0

# unwrap voltage phases for very low voltages
idx = find(DAE.y(Bus.v) < 1e-4)
if not isempty(idx), DAE.y(Bus.a) = rem(DAE.y(Bus.a),2*np.pi); end

# message of end of operations
if iteration >= iter_max
  fm_print('Solution of algebraic equations failed.')
  DAE.y(Bus.a) = angles
  DAE.y(Bus.v) = getnp.ones((Bus))
  DAE.y(getbus(PV,'v')) = getvg(PV,'all')
  DAE.y(getbus(SW,'v')) = getvg(SW,'all')
  conv = 0
elseif Show
  if not isempty(idx)
    [minv,idxv] = min(DAE.y(Bus.v))
    fm_print(['Minimum voltage at bus <',Bus.names{idxv}, ...
             '> = ',num2str(minv)])
  fm_print(['Solution of algebraic equations completed in ', ...
	   num2str(iteration),' iterations.'])

# update time derivatives of state variables
fm_call('i')