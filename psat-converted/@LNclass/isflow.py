# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@LNclass\isflow.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function out = isflow(a,out,k)

global DAE Bus Settings

if not a.n, return, end

nb = DAE.n+DAE.m+2*Bus.n
ns = Settings.nseries

if k <= nb, return, end

# Pij and Pji
if k > nb  and  k < nb + a.n
  h = k - nb
  if a.con(h,14)
    out = out/a.con(h,14)
  elseif a.con(h,15)
    out = out/a.con(h,15)
elseif k > nb + ns  and  k < nb + ns + a.n
  h = k - nb - ns
  if a.con(h,14)
    out = out/a.con(h,14)
  elseif a.con(h,15)
    out = out/a.con(h,15)

# Qij and Qji
if k > nb + 2*ns  and  k < nb + 2*ns + a.n
  h = k - nb - 2*ns
  if a.con(h,15)
    out = out/a.con(h,15)
elseif k > nb + 3*ns  and  k < nb + 3*ns + a.n
  h = k - nb - 3*ns
  if a.con(h,15)
    out = out/a.con(h,15)

# Iij and Iji
if k > nb + 4*ns  and  k < nb + 4*ns + a.n
  h = k - nb - 4*ns
  if a.con(h,13)
    out = out/a.con(h,13)
elseif k > nb + 5*ns  and  k < nb + 5*ns + a.n
  h = k - nb - 5*ns
  if a.con(h,13)
    out = out/a.con(h,13)

# Sij and Sji
if k > nb + 6*ns  and  k < nb + 6*ns + a.n
  h = k - nb - 6*ns
  if a.con(h,15)
    out = out/a.con(h,15)
elseif k > nb + 7*ns  and  k < nb + 7*ns + a.n
  h = k - nb - 7*ns
  if a.con(h,15)
    out = out/a.con(h,15)

