# Module: psat.cli.benchmark
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
# scripts that runs a varieties of benchmarks for testing PSAT

close all
clear all
clear classes

initpsat
clpsat.mesg = 0

# power flow
print('Test 1 - Power flow analysis.')
runpsat('d_006_mdl',[Path.psat,'tests'],'data')

Settings.distrsw = 0
Settings.lftol = 1e-5
Settings.pfsolver = 1
runpsat('pf')
y = [0.0253; 0; -0.0353; -0.0406; -0.0726; -0.0735; ...
     1.0500; 1.0500; 1.0500; 0.9859; 0.9685; 0.9912]
u = max(abs(DAE.y-y))
if u > 1e-4
  print('* * * Newton-Rapshon, single slack bus: Failed!')
else
  print('* * * Newton-Rapshon, single slack bus: OK')

Settings.distrsw = 1
runpsat('pf')
y = [0.0253; 0; -0.0353; -0.0406; -0.0726; -0.0735; ...
     1.0500; 1.0500; 1.0500; 0.9859; 0.9685; 0.9912]
u = max(abs(DAE.y-y))
if u > 1e-4  and  abs(DAE.kg+4.2835e-04) > 1e-6
  print('* * * Newton-Rapshon, distributed slack bus: Failed!')
else
  print('* * * Newton-Rapshon, distributed slack bus: OK')

Settings.distrsw = 0
Settings.pfsolver = 2
runpsat('pf')
Settings.pfsolver = 1
if Settings.iter > 6
  print('* * * Fast decoupled power flow: Failed!')
else
  print('* * * Fast decoupled power flow: OK')

# static report
lasterr('')
try
  runpsat('pfrep')
  print('* * * Static report: OK')
catch
  print(['* * * Static report: Failed!'])
print(' ')

# CPF analysis
print('Test 2 - Continuation power flow analysis.')
CPF.sbus = 1
CPF.linit = 0
CPF.nump = 50
CPF.qlim = 0
CPF.vlim = 0
CPF.ilim = 0
CPF.step = 0.5
CPF.tolc = 1e-5
CPF.type = 1
runpsat('cpf')
if abs(CPF.lambda-11.16) > 0.01
  print('* * * SNB bifurcation: Failed!')
else
  figure
  plot(Varout.t,Varout.vars(:,[7:12]))
  xlabel('lambda')
  ylabel('voltages')
  title('SNB bifurcation')
  print('* * * SNB bifurcation: OK')

CPF.qlim = 1
CPF.sbus = 0
runpsat('cpf')
if abs(CPF.lambda-5.1) > 0.1
  print('* * * LIB bifurcation: Failed!')
else
  figure
  plot(Varout.t,Varout.vars(:,[7:12]))
  xlabel('lambda')
  ylabel('voltages')
  title('LIB bifurcation')
  print('* * * LIB bifurcation: OK')

Settings.freq = 60
Settings.static = 0
clpsat.pq2z = 0
runpsat('d_009_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
CPF.sbus = 1
CPF.linit = 1
CPF.qlim = 0
CPF.hopf = 1
CPF.nump = 200
CPF.step = 0.1
runpsat('cpf')
if abs(CPF.lambda-1.6218) > 1e-3  and  abs(CPF.kg-0.0397) > 1e-4
  print('* * * HB bifurcation: Failed!')
else
  figure
  plot(Varout.t,Varout.vars(:,DAE.n+[10:18]))
  xlabel('lambda')
  ylabel('voltages')
  title('HB bifurcation')
  print('* * * HB bifurcation: OK')
print(' ')

# Optimal power flow analysis
print('Test 3 - Optimal power flow analysis.')
runpsat('d_006_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
OPF.flastart = 1
OPF.enflow = 1
OPF.envolt = 1
OPF.enreac = 1
OPF.method = 2
OPF.flow = 1
OPF.type = 1
OPF.omega = 0
OPF.omega_s = '0'
runpsat('opf')
if abs(OPF.obj+1.2165) > 1.e-4
  print('* * * Social benefit: Failed!')
else
  print('* * * Social benefit: OK')
runpsat('pf')
OPF.omega = 1
OPF.omega_s = '1'
OPF.lmax = 10
Settings.lfmit = 50
runpsat('opf')
Settings.lfmit = 20
if abs(OPF.obj+0.84) > 0.01
  print('* * * Maximum loading condition: Failed!')
else
  print('* * * Maximum loading condition: OK')
print(' ')

# Eigenvalue analysis
print('Test 4 - Small signal stability analysis.')
Settings.freq = 50
Settings.static = 0
clpsat.pq2z = 0
clpsat.readfile = 0
runpsat('d_014_pss_l14_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
Line.store(16,16) = 0
runpsat('pf')
runpsat('sssa')
eig10 = -55.1037 -27.9148i
u = find(abs(SSSA.eigs-eig10) < 1e-4)
z = find(real(SSSA.eigs > 1e-5))
if isempty(u)  and  isempty(z)
  print('* * * Stable case: Failed!')
else
  print('* * * Stable case: OK')

runpsat('d_014_dyn_l14_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
Line.store(16,16) = 0
runpsat('pf')
runpsat('sssa')
eig8 = -51.36-6 - 8.5115i
u = find(abs(SSSA.eigs-eig8) < 1e-4)
z = find(real(SSSA.eigs > 1e-3))
if isempty(u)  and  len(z) != 2
  print('* * * Unstable case: Failed!')
else
  print('* * * Unstable case: OK')
print(' ')

# Time domain simulation
print('Test 5 - Time domain simulation.')
Settings.freq = 60
Settings.fixt = 0
clpsat.readfile = 1
clpsat.pq2z = 1
runpsat('d_009_fault_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
Settings.tf = 20
runpsat('td')
if mean(DAE.y(10:18)) < 0.8 
  print('* * * Fault analysis 1: Failed!')
else
  figure
  plot(Varout.t,Varout.vars(:,DAE.n+[10:18]))
  xlabel('time (s)')
  ylabel('voltages')
  title('Fault analysis 1')
  print('* * * Fault analysis 1: OK')

Settings.fixt = 1
Settings.tstep = 0.05
runpsat('d_014_dyn_l14_mdl',[Path.psat,'tests'],'data')
runpsat('pf')
Settings.tf = 10
clpsat.pq2z = 0
runpsat('td')
if abs(DAE.x(2)-1.0002) > 1e-4   
  print('* * * Fault analysis 2: Failed!')
else
  figure
  plot(Varout.t,Varout.vars(:,[2 7 13 19 25]))
  xlabel('time (s)')
  ylabel('rotor speeds')
  title('Fault analysis 2')
  print('* * * Fault analysis 2: OK')
print(' ')

# Interfaces
print('Test 6 - Interfaces.')
clpsat.readfile = 1
clpsat.pq2z = 1
runpsat('d_006_mdl',[Path.psat,'tests'],'data')
runpsat('pf')

# GAMS
GAMS.method = 3
GAMS.type = 1
GAMS.flow = 1
GAMS.flatstart = 1
[u,w] = system('gams')
if u
  print('* * * GAMS is NOT properly installed on your system.')
else
  runpsat('gams')
  y = [0.0141; 0; -0.0246; -0.0507; -0.0732; -0.0676; ...
       1.1000; 1.1000; 1.1000; 1.0211; 1.0129; 1.0404]
  z = max(abs(DAE.y-y))
  if z > 1e-4
    print('* * * GAMS interface: Failed!')
  else
    print('* * * GAMS interface: OK')

# UWPFLOW
[u,w] = system('uwpflow')
if isempty(strmatch('UW Continuation Power Flow',w))
  print('* * * UWPFLOW is NOT properly installed on your system.')
else
  runpsat('pf')
  DAE.y(12) = 1
  runpsat('uw')
  if abs(DAE.y(12)-0.9912) > 1e-4
    print('* * * UWPFLOW interface: Failed!')
  else
    print('* * * UWPFLOW interface: OK')

print('Testing completed.')



