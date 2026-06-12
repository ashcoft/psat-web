# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@PVclass\gcall.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = gcall(p)

global DAE Bus Settings

if not p.n, return, end

K = p.u.*(1+DAE.kg*p.con(:,10))
DAE.g(p.bus) = DAE.g(p.bus) - K.*p.con(:,4)
if not Settings.pv2pq
  DAE.g(p.vbus(find(p.u))) = 0
  return

# ================================================
# check reactive power limits
# ================================================

# find max mismatch error
if isempty(DAE.g)  or  Settings.iter < Settings.pv2pqniter
  prev_err = 1e6
else
  prev_err = 2*Settings.error
p.newpq = 0

# Q min
# ================================================

# Limit check improved by Lars L. 2006-01.
[tmp,idx] = max(p.u.*(p.con(:,7) - DAE.g(p.vbus) - prev_err))

if tmp > 0
  if not p.pq(idx)
    fm_print(['Switch PV bus <', Bus.names{p.bus(idx)}, '> to PQ bus: Min Qg reached'])
  p.qg(idx) = p.con(idx,7)
  p.pq(idx) = 1
  p.newpq = not Settings.multipvswitch

# Q max
# ================================================

# Limit check improved by Lars L. 2006-01.
[tmp,idx] = min(p.u.*(p.con(:,6) - DAE.g(p.vbus) + prev_err))

if tmp < 0  and  not p.newpq
  if not p.pq(idx)
    fm_print(['Switch PV bus <', Bus.names{p.bus(idx)}, '> to PQ bus: Max Qg reached'])
  p.qg(idx) = p.con(idx,6)
  p.pq(idx) = 1
  p.newpq = not Settings.multipvswitch

# Generator reactive powers
# ================================================

DAE.g(p.vbus) = DAE.g(p.vbus) - p.u.*p.qg
DAE.g(p.vbus(find(not p.pq & p.u))) = 0
