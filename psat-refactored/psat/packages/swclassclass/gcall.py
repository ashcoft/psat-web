# Module: psat.packages.swclassclass.gcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = gcall(p)

global DAE Settings Bus PV

if not p.n, return, end

idx = find(p.u)
DAE.g(p.bus(idx)) = 0
if not Settings.pv2pq 
  DAE.g(p.vbus(idx)) = 0
  return

# ================================================
# check reactive power limits
# ================================================

# find max mismatch error
if isempty(DAE.g)  or  Settings.iter < Settings.pv2pqniter
  prev_err = 1e6
else
  prev_err = 2*Settings.error

# Q min
# ================================================

# Limit check improved by Lars L. 2006-01.
[tmp,idx] = max(p.u.*(p.con(:,7) - DAE.g(p.vbus) - prev_err))

if tmp > 0  and  not PV.newpq
  if not p.dq(idx)
    fm_print(['Switch SW bus <', ...
             Bus.names{p.bus(idx)}, ...
             '> to theta-Q bus: Min Qg reached'])
  p.qg(idx) = p.con(idx,7)
  p.dq(idx) = 1

# Q max
# ================================================

# Limit check improved by Lars L. 2006-01.
[tmp,idx] = min(p.u.*(p.con(:,6) - DAE.g(p.vbus) + prev_err))

if tmp < 0  and  not PV.newpq 
  if not p.dq(idx)
    fm_print(['Switch SW bus <', ...
             Bus.names{p.bus(idx)}, ...
             '> to theta-Q bus: Max Qg reached'])
  p.qg(idx) = p.con(idx,6)
  p.dq(idx) = 1

# Generator reactive powers
# ================================================

DAE.g(p.vbus) = DAE.g(p.vbus) - p.u.*p.qg
DAE.g(p.vbus(find(not p.dq & p.u))) = 0