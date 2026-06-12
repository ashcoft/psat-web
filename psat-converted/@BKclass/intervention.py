# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BKclass\intervention.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = intervention(a,t)

if not a.n, return, end

# do not repeat computations if the simulation is stucking
if a.time != t
  a.time = t
else
  return

global Line Bus

# Toggle Breaker Status

action = {'Opening','Closing'}
idx = [find(a.t1 == t); find(a.t2 == t)]

if not isempty(idx)

  a.u(idx) = not a.u(idx)
for i in range(1, len(idx)+1):
    k = idx(i)
    fm_print([action{a.u(k)+1},' breaker at bus <', ...
             Bus.names{a.bus(k)}, ...
             '> on line from <', ...
             Bus.names{Line.fr(a.line(k))}, ...
             '> to <', ...
             Bus.names{Line.to(a.line(k))}, ...
             '> for t = ',num2str(t),' s'])
    
# update Line data and admittance matrix
    Line = setstatus(Line,a.line(k),a.u(k))
    
# update algebraic variables
#conv = fm_nrlf(40,1e-4,1,1);
  
# checking network connectivity
    fm_flows('connectivity','verbose')

