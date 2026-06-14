# Module: psat.gui.fm_int
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def fm_int():

# FM_INT time domain integration routines:
#       1 - Forward Euler
#       2 - Trapezoidal Method
#
# FM_INT
#
#see also FM_TSTEP, FM_OUT and the Settings structure
#
#Author:    Federico Milano
#Date:      11-Nov-2002
#Update:    16-Jan-2003
#Update:    27-Feb-2003
#Update:    01-Aug-2003
#Update:    11-Sep-2003
#Version:   1.0.4
#
#E-mail:    federico.milano@ucd.ie
#Web-site:  faraday1.ucd.ie/psat.html
#
# Copyright (C) 2002-2016 Federico Milano

global Fig Settings Snapshot Hdl
global Bus File DAE Theme OMIB
global SW PV PQ Fault Ind
global Varout Breaker Line Path clpsat

if not autorun('Time Domain Simulation',1), return, end

tic

# initial messages
# -----------------------------------------------------------------------

fm_disp

if DAE.n == 0  and  not clpsat.init
  Settings.ok = 0
  uiwait(fm_choice('No dynamic component is loaded. Continue anyway?',1))
  if not Settings.ok
    fm_print('Time domain simulation aborted.',2)
    return

fm_print('Time domain simulation')
switch Settings.method
 case 1,
  fm_print('Implicit Euler integration method')
 case 2,
  fm_print('Trapezoidal integration method')
fm_print(['Data file "',Path.data,File.data,'"'])
if not isempty(Path.pert),
  fm_print(['Perturbation file "',Path.pert,File.pert,'"'])
if (strcmp(File.pert,'pert')  and  strcmp(Path.pert,Path.psat))  or  ...
      isempty(File.pert)
  fm_print('No perturbation file set.',1)

if ishandle(Fig.main)
  hdl = findobj(Fig.main,'Tag','PushClose')
  set(hdl,'String','Stop')
  set(Fig.main,'UserData',1)

if Settings.plot
  if Settings.plottype == 1  and  not DAE.n
    Settings.plottype = 2
    fm_print('Cannot plot state variables (dynamic order = 0).')
    fm_print('Bus voltages will be plotted during the TD simulation.')
  maxlegend = min(Bus.n,7)
  switch Settings.plottype
   case 1
    maxlegend = min(DAE.n,7)
    idx0 = 0
   case 2
    idx0 = DAE.n
   case 3
    idx0 = DAE.n+Bus.n
   case 4
    idx0 = DAE.n+DAE.m
   case 5
    idx0 = DAE.n+DAE.m+Bus.n
   case 6
    maxlegend = 3
    idx0 = DAE.n+DAE.m+2*Bus.n

# check settings
# ------------------------------------------------------------------

iter_max = Settings.dynmit
tol = Settings.dyntol
Dn = 1
if DAE.n, Dn = DAE.n; end
identica = spnp.eye(max(Dn,1))

if (Fault.n  or  Breaker.n)  and  PQ.n  and  not Settings.pq2z
  if clpsat.init
    if clpsat.pq2z
      Settings.pq2z = 1
    else
      Settings.pq2z = 0
  elseif not Settings.donotask
    uiwait(fm_choice(['Convert (recommended) PQ loads to constant impedances?']))
    if Settings.ok
      Settings.pq2z = 1
    else
      Settings.pq2z = 0

# convert PQ loads to shunt admittances (if required)
PQ = pqshunt(PQ)

# set up variables
# ----------------------------------------------------------------

DAE.t = Settings.t0
fm_call('i')
DAE.tn = DAE.f
if isempty(DAE.tn), DAE.tn = 0; end

# graphical settings
# ----------------------------------------------------------------

plot_now = 0
if not clpsat.init  or  ishandle(Fig.main)
  if Settings.plot
    if ishandle(Fig.plot)
      figure(Fig.plot)
    else
      fm_plotfig
  elseif Settings.status
    fm_bar('open')
    fm_simtd('init')
    idxo = 0
  else
    fm_print(['t = ',num2str(Settings.t0),' s'],3)
    perc = 0
    perc_old = 0
  drawnow

# ----------------------------------------------------------------
# initializations
# ----------------------------------------------------------------

t = Settings.t0
k = 1
h = fm_tstep(1,1,0,Settings.t0)
inc = np.zeros((Dn+DAE.m,1))
callpert = 1

# get initial network connectivity
fm_flows('connectivity', 'verbose')

# output initialization
fm_out(0,0,0)
fm_out(2,Settings.t0,k)

# time vector of snapshots, faults and breaker events
fixed_times = []

n_snap = len(Snapshot)
if n_snap > 1  and  not Settings.locksnap
  snap_times = np.zeros((n_snap-1,1))
for i in range(2, n_snap+1):
    snap_times(i-1,1) = Snapshot(i).time
  fixed_times = [fixed_times; snap_times]

fixed_times = [fixed_times; gettimes(Fault); ...
               gettimes(Breaker); gettimes(Ind)]
fixed_times = sort(fixed_times)

# compute max rotor angle difference
diff_max = anglediff

# ================================================================
# ----------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------
# ================================================================

inc = np.zeros((Dn+DAE.m,1))

while (t < Settings.tf)  and  (t + h > t)  and  not diff_max
  if ishandle(Fig.main)
    if not get(Fig.main,'UserData'), break, end
  if (t + h > Settings.tf), h = Settings.tf - t; end
  actual_time = t + h

# check not to jump disturbances
  index_times = find(fixed_times > t & fixed_times < t+h)
  if not isempty(index_times)
    actual_time = min(fixed_times(index_times))
    h = actual_time - t

# set global time
  DAE.t = actual_time

# backup of actual variables
  if isempty(DAE.x), DAE.x = 0; end
  xa = DAE.x
  ya = DAE.y

# initialize NR loop
  iterazione = 1
  inc(1) = 1
  if isempty(DAE.f), DAE.f = 0; end
  fn = DAE.f

# applying faults, breaker interventions and perturbations
  if not isempty(fixed_times)
    if not isempty(find(fixed_times == actual_time))
      Fault = intervention(Fault,actual_time)
      Breaker = intervention(Breaker,actual_time)

  if callpert
    try
      if Settings.hostver >= 6
        feval(Hdl.pert,actual_time)
      else
        if not isempty(Path.pert)
          cd(Path.pert)
          feval(Hdl.pert,actual_time)
          cd(Path.local)
    catch
      fm_print('* * Something wrong in the perturbation file:')
      fm_print(lasterr)
      fm_print('* * The perturbation file will be discarded.')
      callpert = 0

# Newton-Raphson loop
  Settings.error = tol+1
  while Settings.error > tol
    if (iterazione > iter_max), break,  end
    drawnow
    if ishandle(Fig.main)
      if not get(Fig.main,'UserData'), break, end

# DAE equations
    fm_call('i')

# complete Jacobian matrix DAE.Ac
    switch Settings.method
     case 1  #  Forward Euler
      DAE.Ac = [identica - h*DAE.Fx, -h*DAE.Fy; DAE.Gx, DAE.Gy]
      DAE.tn = DAE.x - xa - h*DAE.f
     case 2  #  Trapezoidal Method
      DAE.Ac = [identica - h*0.5*DAE.Fx, -h*0.5*DAE.Fy; DAE.Gx, DAE.Gy]
      DAE.tn = DAE.x - xa - h*0.5*(DAE.f + fn)

# Non-windup limiters
    fm_call('5')
    inc = -DAE.Ac\[DAE.tn; DAE.g]

#inc = -umfpack(DAE.Ac,'\',[DAE.tn; DAE.g]);
    DAE.x = DAE.x + inc(1:Dn)
    DAE.y = DAE.y + inc(1+Dn: DAE.m+Dn)
    iterazione = iterazione + 1
    Settings.error = max(abs(inc))

  if (iterazione > iter_max)
    h = fm_tstep(2,0,iterazione,t)
    DAE.x = xa
    DAE.y = ya
    DAE.f = fn
  else
    h = fm_tstep(2,1,iterazione,t)
    t = actual_time
    k = k+1
# extend output stack
    if k > len(Varout.t), fm_out(1,t,k); end

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# update output variables, snapshots and network visualisation
# ----------------------------------------------------------------
# ----------------------------------------------------------------

    fm_out(2,t,k)

#  plot variables & display iteration status
# ----------------------------------------------------------------

    i_plot = 1+k-10*fix(k/10)
    perc = (t-Settings.t0)/(Settings.tf-Settings.t0)
    if i_plot == 10
      fm_print([' > Simulation time = ',num2str(DAE.t), ...
	       ' s (',num2str(round(perc*100)),'%)'])

    if not clpsat.init  or  ishandle(Fig.main)
      if Settings.plot
        if i_plot == 10
          plot(Varout.t(1:k),Varout.vars(1:k,idx0+[1:maxlegend]))
          set(gca,'Color',Theme.color11)
          xlabel('time (s)')
          drawnow
      elseif Settings.status
        idx = (t-Settings.t0)/(Settings.tf-Settings.t0)
        fm_bar([idxo,idx])
        if i_plot == 10, fm_simtd('update'), end
        idxo = idx

# fill up snapshots
    if n_snap > 1  and  not Settings.locksnap
      snap_i = find(snap_times == t)+1
      fm_snap('assignsnap',snap_i)


# compute max rotor angle difference
  diff_max = anglediff


if Settings.status  and  not Settings.plot
  fm_bar('close')
  fm_simtd('update')
if not DAE.n, DAE.x = []; DAE.f =[]; end

# final messages
# -----------------------------------------------------------------------

if ishandle(Fig.main)
  if diff_max  and  get(Fig.main,'UserData')
    fm_print(['Rotor angle max difference is > ', ...
             num2str(Settings.deltadelta), ...
             ' deg. Simulation stopped at t = ', ...
             num2str(t), ' s'],2)
  elseif (t < Settings.tf)  and  get(Fig.main,'UserData')
    fm_print(['Singularity likely. Simulation stopped at t = ', ...
             num2str(t), ' s'],2)
  elseif not get(Fig.main,'UserData')
    fm_print(['Dynamic Simulation interrupted at t = ',num2str(t),' s'],2)
  else
    fm_print(['Dynamic Simulation completed in ',num2str(toc),' s'])
else
  if diff_max
    fm_print(['Rotor angle max difference is > ', ...
             num2str(Settings.deltadelta), ...
             ' deg. Simulation stopped at t = ', ...
             num2str(t), ' s'],2)

  elseif (t < Settings.tf)
    fm_print(['Singularity likely. Simulation stopped at t = ', ...
             num2str(t), ' s'],2)
  else
    fm_print(['Dynamic Simulation completed in ',num2str(toc),' s'])

# resize output varibales & final settings
# -----------------------------------------------------------------------

fm_out(3,t,k)
if Settings.beep, beep, end
Settings.xlabel = 'time (s)'
if ishandle(Fig.plot), fm_plotfig, end

# future simulations do not need LF computation
Settings.init = 2
SNB.init = 0
LIB.init = 0
CPF.init = 0
OPF.init = 0
if ishandle(Fig.main), set(hdl,'String','Close'); end
DAE.t = -1; #  reset global time

# compute delta difference at each step
# -----------------------------------------------------------------------
function diff_max = anglediff
global Settings Syn Bus DAE SW OMIB

diff_max = 0

if not Settings.checkdelta, return, end
if not Syn.n, return, end

delta = DAE.x(Syn.delta)
[idx,ia,ib] = intersect(Bus.island,getbus(Syn))
if not isempty(idx), delta(ib) = []; end

if isscalar(delta)
  delta = [delta; DAE.y(SW.refbus)]
delta_diff = abs(delta-min(delta))
diff_max = (max(delta_diff)*180/np.pi) > Settings.deltadelta
if diff_max, return, end

# check transient stability
#fm_omib
#if abs(OMIB.margin) > 1e-2
#  fm_disp(['* * Transient stability margin: ',num2str(OMIB.margin)])
#end