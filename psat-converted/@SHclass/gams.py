# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SHclass\gams.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [Gh,Bh,Ghc,Bhc] = gams(a,method,Gh,Bh,Ghc,Bhc)

global Bus GAMS Settings

if not a.n, return, end

nb = Bus.n

if method != 1
  Gh = Gh + sparse(a.bus,a.bus,a.u.*a.con(:,5),nb,nb)
  Bh = Bh + sparse(a.bus,a.bus,a.u.*a.con(:,6),nb,nb)

if method == 4  or  method == 6  or  method == 7
  Ghc = Ghc + sparse(a.bus,a.bus,a.u.*a.con(:,5),nb,nb)
  Bhc = Bhc + sparse(a.bus,a.bus,a.u.*a.con(:,6),nb,nb)
